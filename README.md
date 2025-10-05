# 🛰️ Distributed Log Processing System

A scalable, cloud-native **Distributed Log Processing Platform** designed to ingest, process, and analyze logs in real time.

This system demonstrates a full-fledged **distributed data pipeline** that integrates:
- Log ingestion and validation via **FastAPI**
- Stream buffering using **Kafka**
- Real-time data processing and unification with **Apache Flink**
- Analytical storage through **ClickHouse**
- Fast caching and live data serving via **Redis**
- Future support for **AI-driven anomaly detection and summarization**

---

## ⚙️ Overview

**Goal:**
Build a horizontally scalable, fault-tolerant, and extensible log analytics platform capable of handling massive log streams from distributed systems.

**Key Features:**
- Unified log schema for structured analysis
- Stream-based processing for real-time insights
- Low-latency analytical storage and querying
- Caching for live dashboards and API acceleration
- Cloud-deployable architecture (GCP-ready)

---

## 🏗️ Architecture

<p align="center">
  <img src="/docs/architecture.png" alt="Architecture Diagram" width="800"/>
</p>

**Flow Summary:**
1. **FastAPI** receives logs from services and publishes them to **Kafka**.
2. **Flink** consumes Kafka streams, normalizes formats, enriches metadata, and outputs to:
   - **ClickHouse** for analytical storage
   - **Redis** for quick-access caching
3. (Planned) **AI layer** will consume processed streams for anomaly detection and summarization.

---

## 🧰 Tech Stack

| Component | Technology | Purpose |
|------------|-------------|----------|
| **Language** | Python | Core development |
| **Ingestion Service** | FastAPI | Log intake and validation |
| **Message Queue** | Apache Kafka | Distributed log transport |
| **Stream Processing** | Apache Flink (PyFlink) | Real-time ETL & schema unification |
| **Database** | ClickHouse | Analytical log storage |
| **Cache** | Redis | Real-time dashboard cache |
| **Cloud Platform** | Google Cloud Platform (GCP) | Deployment and scalability |

---

## 💡 Summary

This project establishes the foundation for a **real-time, distributed log analytics system** that’s:
- Scalable across multiple compute and data layers
- Fault-tolerant through Kafka + Flink checkpointing
- Extensible for AI-driven insights and summarization
