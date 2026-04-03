# Архитектура центрального сервиса: PortfolioService

## Диаграмма архитектуры (гексагональная)

```plantuml
@startuml
skinparam handwritten true
skinparam packageStyle rectangle

title PortfolioService - Hexagonal Architecture

package "Infrastructure Layer" {
    class PortfolioController <<Inbound Adapter>> {
        + get_profitability(portfolio_id, period)
    }

    class InMemoryPortfolioRepository <<Outbound Adapter>> {
        + save(portfolio)
        + find_by_id(id)
    }

    class FakeMarketDataService <<Outbound Adapter>> {
        + get_current_price(ticker)
    }
}

package "Application Layer" {
    interface CalculateProfitabilityUseCase <<Inbound Port>> {
        + calculate(portfolio_id, period_start, period_end)
    }

    class PortfolioService <<Application Service>> {
        - repository
        - market_data
        + calculate(portfolio_id, period_start, period_end)
    }

    interface PortfolioRepository <<Outbound Port>> {
        + save(portfolio: Portfolio)
        + find_by_id(id: str): Portfolio
    }

    interface MarketDataService <<Outbound Port>> {
        + get_current_price(ticker: str): float
    }
}

package "Domain Layer" {
    class Portfolio <<Domain Entity>> {
        + id: str
        + positions: list
        + add_transaction(transaction)
        + calculate_value(prices)
    }

    class Position <<Domain Entity>> {
        + ticker: str
        + amount: int
        + average_price: float
    }

    class Transaction <<Domain Entity>> {
        + id: str
        + type: str
        + volume: int
        + price: float
    }
}

PortfolioController ..> CalculateProfitabilityUseCase : использует

CalculateProfitabilityUseCase <|.. PortfolioService : реализует
PortfolioService --> PortfolioRepository : зависит
PortfolioService --> MarketDataService : зависит
PortfolioService ..> Portfolio : манипулирует

PortfolioRepository <|.. InMemoryPortfolioRepository : реализует
MarketDataService <|.. FakeMarketDataService : реализует

Portfolio "1" *-- "many" Position
Portfolio "1" *-- "many" Transaction

@enduml
```

## Объяснение портов

**Входящие порты (Inbound Ports):**
- `CalculateProfitabilityUseCase`: Служит точкой входа для операций расчета доходности (например, из контроллера REST или gRPC). Определяет метод, принимающий ID портфеля и временной период, и возвращающий финансовый отчет.

**Исходящие порты (Outbound Ports):**
- `PortfolioRepository`: Выступает интерфейсом хранилища (базы данных) портфелей. Его реализуют конкретные адаптеры (например, `InMemoryPortfolioRepository`).
- `MarketDataService`: Интерфейс для взаимодействия со сторонним сервисом (API) рыночных цен. Он позволяет приложению запрашивать котировки без привязки к конкретному HTTP-клиенту.

## Принципы SOLID

- **Dependency Inversion Principle (DIP)**: `PortfolioService` зависит от абстракций `PortfolioRepository` и `MarketDataService`, а не от их реализаций. Сама реализация внедряется через DI.
- **Single Responsibility Principle (SRP)**: Доменный слой (сущности) отвечают только за представление данных и внутренние расчеты; Application-слой оркестрирует процесс получения данных; Infrastructure-слой отвечает за ввод/вывод и REST/БД.
