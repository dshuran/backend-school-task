# Задание в бэкэнд школу Яндекса

## Вступление

Добрый день, на связи Дмитрий Шуран. Считаю, что небольшое предисловие
всё-таки необходимо. 

Коротко о себе: студент МАИ, фронт-энд разработчик, стажируюсь чуть менее года года в
центре молодых специалистов 1С. Чуть подробнее [здесь](https://github.com/dshuran/CV)

Познакомился с питоном ~ 9 августа. Чуть позже, уже после 12-го августа произошло
знакомство с базами данных, REST сервисами, ORM, Flask'ом. В общем,
вы поняли :) 

Как следствие, мой код может немного (или много) не соответствовать
стилю программирования на питоне и каким-либо другим принятым стандартам.
Просьба принять это во внимание. 
 
И последнее, о чём хочется сказать. Ребят, спасибо вам за контест,
тестовое задание. Узнал очень много всего нового за эти пару недель, это 
было круто! Отдельный респект за очень быстрые ответы на все вопросы по
электронной почте. А теперь, давайте же приступим! 
 
## Выбор фреймворка, базы данных и архитектуры проекта
 
Говоря о фреймворке, выбор был сделан в пользу `Flask` из-за того, что он 
(по крайней мере на первый взгляд) предоставляет большую гибкость, чем `Django`.
 
В качестве средства для работами с базами данных выбор был сделан в пользу 
`SQLAlchemy`. 
 
Что касается баз данных: я рассматривал два варианта `PostgreSQL` и `SQLite`.
И по крайней мере на данном этапе выбор был сделан в пользу последней.
Мои тесты показали, что она работает немного быстрее в данном проекте
(хотя может быть тому причиной мои руки). Кроме того, она немного удобнее
в использовании. Создаётся в корне проекта.

Расположение функций и классов по файлам произведено
исходя из модели `MVC` (Model View Controller). 

Кроме того, я попытался избежать различных циклических зависимостей,
которые возникали по ходу проекта. Как следствие, я частично использовал
паттерн [Application Factory](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/).

По ходу проектирования старался так создавать и использовать функции, чтобы
как можно меньшее кол-во деталей зависело от их непосредственной реализации.
Это оказалось весьма удобным в ходе дальнейшей модификации. Одним словом,
некоторые из принципов `SOLID` здесь тоже задействованы.
 
 ## Установка
 
 Для запуска проекта на своей машине необходимо выполнить несколько простых
 шагов: 
 1. Склонировать данный репозиторий на рабочую машину
 2. Произвести установку виртуальной среды для данного проекта
 3. Запустить `app.py` при необходимости указав собственные `host` и `port` в
 качестве аргументов `app.run()`
 4. Сервер запущен! 
 
 ## Тестирование
 
 Для тестирования была создана специальная директория `Tests`. 
 
 ### Конфигурация тестовых скриптов
 
 #### Генерация жителей
 Внутри функции `main` файла `citizens_generator.py` мы запускаем функцию
  `generate_post_requests_input`. Вы можете произвольно менять её
  аргументы по своему усмотрению:
  1. `requests_amount` - количество запросов, которое мы хотим послать,
  другими словами -- количество создаваемых тестовых файлов.
  2. `citizens_amount` -- количество жителей в каждом запросе.
  3. `max_relatives` -- максимальное количество родственников с небольшим
  разбросом. Т.е. кол-во родственников может быть `max_relatives` +- `eps`,
  где `eps` -- небольшое целое число. Это особенность реализации, которая
  служит для большей рандомизации создаваемых жителей. 
  
 #### Установка крайних значений номеров выгрузок
 Следует обратить внимание на переменные `min_id` и `max_id` метода
 `test_requests`. Они задают количество выгрузок на отрезке [`min_id`, `max_id`],
 которое будет тестироваться.
 
 ### Запуск тестов 
 Инструкция по использованию следующая:
 (**рекомендуется сначала сконфигурировать скрипты под себя! См. выше**)
 1. Запустить скрипт `create_test_dirs.py`. Он создаст все необходимые папки.
 2. Запустить скрипт `citizens_generator.py`. Он генерирует жителей
 корректного формата, объединяет их в массив и складывает по пути 
 `post_requests/input`. 
 3. Запустить скрипт `run_tests.py`. Он начинает запуск тестов.
 
 ### Комментарий по тестам
 
 Фактически, мы лишь проверяем, что мы получили корректный ответ на запрос
 от сервера. Однако, можно наоброт посылать некорректные входные данные и
 проверять, что запрос неверный. Данная возможность здесь реализована
 частично: поле `good_request` метода `request_sender` внутри `run_tests.py `.
 Аналогично существует возможность создавать некорректных жителей при помощи
 метода `get_incorrect_citizen` скрипта `citizens_generator.py`.
 Присутствуют и другие незадокументированные возможности юнит-тестирования,
 однако они кажутся излишними в пределах данного проекта, поскольку
 валидация показала себя очень хорошо в ходе ручного запуска множества тестов. 
 
 Считаю, что намного более показательными являются тесты производительности.
 В ходе тестирования на больших данных выяснились "узкие" места в коде. 
 В частности были исправлены следующие проблемы:
 1. Скорость валидации входных данных увеличилась ~ в два раза за счёт 
 подключения другой библиотеки (подробнее см. в описании зависимостей)
 2. Скорость обработки запроса на расчёт подарков увеличилась ~ в 100 раз
 за счёт хранения некоторых данных в оперативной памяти вместо базы данных.
 
 
## Валидации

Все входные данные проходят несколько этапов валидации. Далее идёт описание
некоторых из них.

### Валидация входных данных

#### POST запрос

На начальном этапе мы проверяем корректность формата JSON на входе.
Если данные корректны, то запускается валидация данных при помощи модуля,
который реализует [JSON Schema](https://json-schema.org/). Однако было
выявлена, что модуль работает недостаточно быстро, поэтому было решено 
использовать `fastjsonschema`


 