import os
import random
import torch
import numpy as np
import pandas as pd
from datasets import Dataset, concatenate_datasets
from transformers import DataCollatorForSeq2Seq
from unsloth import FastLanguageModel, is_bfloat16_supported, UnslothTrainingArguments
from trl import SFTTrainer

# 데이터셋 경로
IT_LOCAL_DATA = [
    "./data/sft_data/translated_Hanhhanh9_QA-AI.csv",
    "./data/sft_data/translated_Harikrishnan46624_AI_QA_Data.csv",
    "./data/sft_data/translated_mjphayes_machine_learning_questions.csv",
    "./data/sft_data/translated_prsdm_Machine-Learning-QA-dataset.csv",
    "./data/sft_data/translated_team-bay_data-science-qa.csv",
    "./data/sft_data/translated_whiteOUO_Ladder-machine-learning-QA.csv"
]

# 전처리 함수: Question과 Answer를 결합하여 text 생성
def preprocess_question_answer(example):
    return {"text": f"질문: {example['Question']}\n답변: {example['Answer']}"}

# 데이터 로드 및 전처리
def load_and_preprocess_datasets(dataset_paths, preprocess_fn):
    dataset = Dataset.from_dict({})
    for path in dataset_paths:
        raw_dataset = Dataset.from_pandas(pd.read_csv(path))
        
        # Question, Answer에서 text 필드 생성
        raw_dataset = raw_dataset.map(preprocess_fn, remove_columns=raw_dataset.column_names)
        
        # 기존 데이터셋과 병합
        dataset = concatenate_datasets([dataset, raw_dataset])
    return dataset

# Argument 설정
class Args:
    model = "unsloth/Qwen2.5-7B-Instruct"
    seed = 42
    max_token_length = 2048
    use_cache = True

    lora_r = 64
    lora_alpha = 32
    lora_dropout = 0.0
    lora_target_modules = "q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj"
    use_rslora = False

    epochs = 1
    batch_size = 4
    lr = 1e-4
    lr_scheduler = "linear"
    lr_warmup_ratio = 0.06
    weight_decay = 1e-2
    max_grad_norm = 1.0
    use_gradient_checkpointing = True

args = Args()

# Seed 설정
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

# 실행 메인 함수
if __name__ == "__main__":
    # Seed 설정
    set_seed(args.seed)

    # 모델 및 토크나이저 로드
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

    # 데이터 로드 및 전처리
    dataset = load_and_preprocess_datasets(IT_LOCAL_DATA, preprocess_question_answer)
    test_size = len(dataset) % args.batch_size if len(dataset) % args.batch_size != 0 else args.batch_size
    dataset = dataset.train_test_split(test_size=test_size, shuffle=True, seed=args.seed)
    train_dataset = dataset["train"].shuffle()
    val_dataset = dataset["test"].shuffle()

    # Data Collator 설정
    data_collator = DataCollatorForSeq2Seq(
        tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True
    )

    # 학습 Argument 설정
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
        output_dir="./adapters/qa-lora",
        report_to="wandb"
    )

    # Trainer 설정 및 학습
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
    trainer.train()
