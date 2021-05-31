# CBR REST currency conversion

#### Сервис для получения курса валют центробанка по средствам REST

К сожалению, на данный момент получать данные по курсам валют от центробанка напрямую
возможно только через SOAP. Данное приложение призвано облегчить получение курсов валют
центробанка, предоставляя удобный REST интерфейс.

Для установки и запуска приложения необходимо чтобы на компьютере был установлен docker-compose

Для первого запуска приложения из текущей папки необходимо вызвать следующие команды: 
```
docker-compose build
docker-compose up
```

Для последующих запусков:
```
docker-compose up
```

Для просмотра документации API после запуска можно перейти в браузере по
адресу `http://localhost:8000/docs`, там же можно попробовать отправить запрос к API


На данный момент доступен только эндпоинт на получение курса валют за определённый день,
с предложениями по улучшению добро пожаловать в пулл реквесты или на [почту](mailto:korid24.dev@gmail.com)