from django.db import models

# Create your models here.

class CauDieuKien(models.Model):
    name = models.CharField(max_length=255)  # Tên điều kiện
    description = models.TextField()  # Mô tả chi tiết điều kiện
    recipe = models.TextField(blank=True, null=True)  # Công thức, có thể để trống
    theuse = models.TextField(blank=True, null=True)  # Cách sử dụng, có thể để trống
    example = models.TextField(blank=True, null=True)  # Ví dụ, có thể để trống
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo
    updated_at = models.DateTimeField(auto_now=True)  # Thời gian cập nhật

    class Meta:
        db_table = 'cau_dieu_kien'

class Word(models.Model):
    name = models.CharField(max_length=255)  # Tên của từ
    meaning = models.TextField()  # Nghĩa của từ
    example_sentence = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo
    updated_at = models.DateTimeField(auto_now=True)  # Thời gian cập nhật

    class Meta:
        db_table = 'word' 

class Tense(models.Model):
    name = models.CharField(max_length=255)
    define = models.TextField()
    formula = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    example = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo
    updated_at = models.DateTimeField(auto_now=True)  # Thời gian cập nhật
    
    class Meta:
        db_table = 'tense'

class Question(models.Model):
    question_text = models.CharField(max_length=255)  # Câu hỏi
    option_a = models.CharField(max_length=255)  # Lựa chọn A
    option_b = models.CharField(max_length=255)  # Lựa chọn B
    option_c = models.CharField(max_length=255)  # Lựa chọn C
    correct_answer = models.CharField(max_length=1)  # Câu trả lời đúng (A, B, C)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question'

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name        