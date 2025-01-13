import os
import random
import argparse
import torch
import numpy as np
from datasets import Dataset, concatenate_datasets
from transformers import DataCollatorForSeq2Seq
from trl import SFTTrainer
from unsloth import FastLanguageModel, is_bfloat16_supported, UnslothTrainingArguments

# JSON 데이터 전처리 함수
def format_choice_question(example):
    choices_text = "\n".join(
        [f"{idx + 1}. {choice}" for idx, choice in enumerate(example["choices"])]
    )
    return {
        "text": f"Question: {example['question']}\nChoices:\n{choices_text}\nAnswer: {example['answer']}"
    }

# IT_LOCAL_DATA 정의
IT_LOCAL_DATA = [
    ("./data/sample_choice_questions.json", (format_choice_question,))
]

def parse_args():
    parser = argparse.ArgumentParser()

    # 모델 설정
    parser.add_argument("--model", default="unsloth/Qwen2.5-7B-Instruct", type=str)
    parser.add_argument("--seed", default=42, type=int)
    parser.add_argument("--max_token_length", default=2048, type=int)
    parser.add_argument("--use_cache", action='store_true')

    # LoRA 설정
    parser.add_argument("--lora_r", default=64, type=int)
    parser.add_argument("--lora_alpha", default=32, type=int)
    parser.add_argument("--lora_dropout", default=0.0, type=float)
    parser.add_argument("--lora_target_modules", default="q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj", type=str)
    parser.add_argument("--use_rslora", action="store_true")

    # 학습 설정
    parser.add_argument("--epochs", default=1, type=int)
    parser.add_argument("--batch_size", default=4, type=int)
    parser.add_argument("--lr", default=1e-4, type=float)
    parser.add_argument("--lr_scheduler", default="linear", type=str)
    parser.add_argument("--lr_warmup_ratio", default=0.06, type=float)
    parser.add_argument("--weight_decay", default=1e-2, type=float)
    parser.add_argument("--max_grad_norm", default=1.0, type=float)
    parser.add_argument("--use_gradient_checkpointing", action='store_true')

    args = parser.parse_args()
    return args

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

if __name__ == "__main__":
    # 인자 파싱
    args = parse_args()

    # 시드 설정
    set_seed(args.seed)

    # 모델과 토크나이저 로드
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        dtype=None,
        load_in_4bit=True,
        max_seq_length=args.max_token_length,
        device_map="auto"
    )
    model.config.use_cache = args.use_cache
    tokenizer.padding_side = "left"

    # LoRA 설정
    lora_target_modules = list(map(lambda x: x.strip(), args.lora_target_modules.split(",")))
    model = FastLanguageModel.get_peft_model(
        model,
        r=args.lora_r,
        target_modules=lora_target_modules,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        use_gradient_checkpointing=args.use_gradient_checkpointing,
        random_state=args.seed,
        use_rslora=args.use_rslora, 
        loftq_config=None
    )

    # 데이터 로드 및 처리
    dataset = Dataset.from_dict({})
    for path, preprocess_fns in IT_LOCAL_DATA:
        with open(path, "r") as f:
            data = json.load(f)
        raw_dataset = Dataset.from_dict(data)
        for preprocess_fn in preprocess_fns:
            preprocessed_dataset = raw_dataset.map(preprocess_fn, remove_columns=raw_dataset.column_names)
            dataset = concatenate_datasets([dataset, preprocessed_dataset])

    # 데이터셋 분리
    test_size = len(dataset) % args.batch_size if len(dataset) % args.batch_size != 0 else args.batch_size
    dataset = dataset.train_test_split(test_size=test_size, shuffle=True, seed=args.seed)

    train_dataset = dataset["train"].shuffle()
    val_dataset = dataset["test"].shuffle()

    # 데이터 Collator 설정
    data_collator = DataCollatorForSeq2Seq(
        tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True
    )

    # 학습 설정
    training_args = UnslothTrainingArguments(
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=args.batch_size,
        num_train_epochs=args.epochs,
        gradient_checkpointing=args.use_gradient_checkpointing,
        max_grad_norm=args.max_grad_norm,
        learning_rate=args.lr,
        lr_scheduler_type=args.lr_scheduler,
        warmup_ratio=args.lr_warmup_ratio,
        weight_decay=args.weight_decay,
        optim="adamw_8bit",
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=1,
        eval_steps=100,
        save_strategy="epoch",
        seed=args.seed,
        output_dir="./adapters/it-lora",
        report_to="wandb"
    )

    # Trainer 설정
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        max_seq_length=args.max_token_length,
        dataset_text_field="text",
        data_collator=data_collator,
        args=training_args
    )

    # 학습 시작
    trainer.train()
