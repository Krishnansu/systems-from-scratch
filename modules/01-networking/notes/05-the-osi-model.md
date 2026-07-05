# Lesson 05 - The OSI Model: Why Networking Is Layered

## Objectives
- Understand why networking is divided into layers.
- Learn the purpose of the OSI Model.
- Understand the responsibility of each layer.
- Understand encapsulation and decapsulation.

## OSI Stack

```text
+---------------------------+
| 7. Application            |
+---------------------------+
| 6. Presentation           |
+---------------------------+
| 5. Session                |
+---------------------------+
| 4. Transport              |
+---------------------------+
| 3. Network                |
+---------------------------+
| 2. Data Link              |
+---------------------------+
| 1. Physical               |
+---------------------------+
```

## Responsibilities

| Layer | Responsibility |
|-------|----------------|
| Application | Network services for applications |
| Presentation | Encoding, Compression, Encryption |
| Session | Session establishment and management |
| Transport | Reliability, Ordering, Flow Control |
| Network | Routing and IP Addressing |
| Data Link | Frames, MAC Addressing |
| Physical | Transmission of Bits |

## Encapsulation

```text
Application Data
        │
        ▼
Application
        ▼
Presentation
        ▼
Session
        ▼
Transport
        ▼
Network
        ▼
Data Link
        ▼
Physical
        ▼
Bits on Wire
```

## Why Layering?
- Separation of concerns
- Easier maintenance
- Interoperability
- Modular implementations
- Easier troubleshooting

## Key Takeaways
- OSI is a conceptual model.
- Each layer has one well-defined responsibility.
- Data moves downward through encapsulation and upward through decapsulation.
- Layering enables interoperability across vendors.

## Reflection
1. Why is layering useful?
2. Which layer handles routing?
3. Why doesn't the Physical layer know about HTTP?
4. How does encapsulation relate to the OSI model?
