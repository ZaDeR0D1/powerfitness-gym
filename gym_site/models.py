from django.db import models

class Coach(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    specialization = models.CharField(max_length=100, verbose_name="Специализация")
    bio = models.TextField(verbose_name="Биография")
    photo = models.ImageField(upload_to='coaches/', verbose_name="Фото", blank=True)
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self):
        return self.name

class Program(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    duration = models.CharField(max_length=50, verbose_name="Продолжительность")
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, verbose_name="Тренер")
    image = models.ImageField(upload_to='programs/', verbose_name="Изображение", blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name="Уровень")

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.name} - {self.subject}"