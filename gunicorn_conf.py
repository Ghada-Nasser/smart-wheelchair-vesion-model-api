import multiprocessing
import os

# بيحدد عدد العمال بناءً على قوة السيرفر
workers_per_core = 2
cores = multiprocessing.cpu_count()
workers = workers_per_core * cores
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
keepalive = 120
timeout = 120 # مهم عشان موديلات الـ AI بتاخد وقت في التحليل
worker_class = "uvicorn.workers.UvicornWorker"