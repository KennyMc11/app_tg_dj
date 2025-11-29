import json
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Простое хранилище в памяти (в продакшене используйте БД)
games = {}

def game_page(request):
    """Главная страница игры"""
    return render(request, 'game.html')

@csrf_exempt
def start_game(request):
    """Начать новую игру"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            # Генерируем случайное число от 1 до 100
            secret_number = random.randint(1, 100)
            games[user_id] = {
                'secret_number': secret_number,
                'attempts': 0,
                'game_over': False
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Игра началась! Угадай число от 1 до 100'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def make_guess(request):
    """Сделать попытку угадать число"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            guess = data.get('guess')
            
            if user_id not in games:
                return JsonResponse({'success': False, 'error': 'Игра не начата'})
            
            game = games[user_id]
            
            if game['game_over']:
                return JsonResponse({'success': False, 'error': 'Игра уже завершена'})
            
            try:
                guess = int(guess)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Введите число'})
            
            game['attempts'] += 1
            
            if guess < game['secret_number']:
                message = '📈 Слишком маленькое число! Попробуй больше'
            elif guess > game['secret_number']:
                message = '📉 Слишком большое число! Попробуй меньше'
            else:
                message = f'🎉 Поздравляю! Ты угадал число {game["secret_number"]} за {game["attempts"]} попыток!'
                game['game_over'] = True
            
            return JsonResponse({
                'success': True,
                'message': message,
                'attempts': game['attempts'],
                'game_over': game['game_over']
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})