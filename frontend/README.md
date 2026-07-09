# Инвестиционный помощник — Frontend

Веб-интерфейс на Next.js + TypeScript + SCSS-модули.

## Запуск

```bash
npm install
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000)

## Сборка

```bash
npm run build
npm start
```

## Структура

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout (шрифты Montserrat + IBM Plex Sans)
│   │   ├── page.tsx                # Главная страница (демо всех компонентов)
│   │   ├── page.module.scss
│   │   └── globals.scss
│   ├── components/
│   │   ├── DashboardHeader/        # Шапка с KPI-плитками
│   │   ├── InvestmentCard/         # Карточка объекта инвестиций
│   │   ├── SupportProgramBadge/    # Тег меры поддержки
│   │   ├── ChatInterface/          # Чат с агентом
│   │   ├── ApplicationStatus/      # Виджет этапов заявки
│   │   ├── Sidebar/                # Левый сайдбар с историей
│   │   └── Skeleton/               # Загрузочные скелетоны
│   ├── styles/
│   │   ├── _variables.scss         # Дизайн-токены (цвета, тени, радиусы)
│   │   └── _mixins.scss            # Переиспользуемые миксины
│   └── types/
│       └── index.ts                # TypeScript типы
├── package.json
├── tsconfig.json
└── next.config.js
```

## Дизайн-система

| Токен | Значение |
|-------|----------|
| Primary | `#0B1F3B` |
| Accent | `#C8A96E` |
| Background | `#F5F6FA` |
| Card | `#FFFFFF` |
| Shadow subtle | `0px 4px 12px rgba(0,0,0,0.04)` |
| Shadow hover | `0px 8px 20px rgba(0,0,0,0.08)` |
| Radius | `8px` |
| Transition | `cubic-bezier(0.4, 0, 0.2, 1) 0.3s` |
| Sidebar | `280px` |
| Max content | `1280px` |

## Компоненты

### DashboardHeader
Шапка дашборда с KPI: активные проекты, общий бюджет, доступные гранты, рабочие места. Каждая плитка имеет иконку, значение с tabular-nums и тренд-индикатор.

### InvestmentCard
Карточка объекта инвестиций: фото 16:9, статусный бейдж, метрики (IRR, NPV, рабочие места), прогресс-бар с градиентом, теги мер поддержки. Поддерживает компактный режим для встраивания в чат.

### SupportProgramBadge
Цветовой тег меры поддержки. Типы: financial (золотой), tax (синий), infrastructure (зелёный), advisory (фиолетовый).

### ChatInterface
Минималистичный чат: облачка сообщений (пользователь — тёмно-синий справа, агент — белый слева с аватаром), индикатор набора, поле ввода с нижней границей. Сообщения агента могут содержать встроенные InvestmentCard.

### ApplicationStatus
Виджет отслеживания этапов заявки: вертикальный timeline с шагами (completed → current → pending), иконки статусов, даты.

## Технологии

- Next.js 14 (App Router)
- TypeScript (strict)
- SCSS Modules
- Phosphor Icons (thin weight)
- next/font (Montserrat, IBM Plex Sans)
