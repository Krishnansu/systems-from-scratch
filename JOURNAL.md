
## Lesson 1 – What is the Internet?

**Date:** 2026-07-05

### What I Learned

The Internet is not a single network. It is a collection of independent networks connected using standardized protocols like TCP/IP.

### Key Insight

Understanding systems starts by understanding the problems they were designed to solve.

### Questions

- How do routers know where to send packets?
- What exactly is inside a packet?
- How do computers discover each other?

---

# Lesson 01 - What is the Internet?

**Date:** 2026-07-05

## What I Learned
The Internet is a decentralized network of interconnected networks communicating using TCP/IP.

## Questions
- How do routers forward packets?
- How does DNS work?

---

# Lesson 02 - What is a Network?

**Date:** 2026-07-05

## What I Learned
A network is a collection of devices that communicate using communication media and standardized protocols. The Internet is one example of a network, but networks can also exist independently.

## Questions
- How are devices uniquely identified on a network?
- How does a router decide where to send packets?

---

# Lesson 03 - How Does Data Travel Across a Network?

**Date:** 2026-07-05

## What I Learned
Application data is converted into binary, divided into packets, transmitted as physical signals by the NIC, forwarded by networking devices, and reassembled at the destination.

## Questions
- How does TCP detect lost packets?
- How are packets ordered correctly at the receiver?

---

# Lesson 04 - Bits, Frames, and Packets: The Units of Network Communication

**Date:** 2026-07-05

## What I Learned
Networking uses different units at different layers. Bits represent physical signals, frames move data across a local network, and packets enable communication across multiple networks through encapsulation and decapsulation.

## Questions
- What information is contained in an Ethernet frame?
- How does encapsulation map to the OSI model?

---

# Lesson 05 - The OSI Model

**Date:** 2026-07-05

## What I Learned
The OSI model divides networking into seven conceptual layers, each responsible for one aspect of communication. Layering makes networking modular, scalable and easier to debug.

## Questions
- Why was the OSI model never implemented directly?
- Which OSI layers correspond to modern protocols?

---

# Lesson 06 - The TCP/IP Model

**Date:** 2026-07-05

## What I Learned
The Internet is built on the TCP/IP model rather than the OSI model. The four-layer architecture maps real-world protocols such as HTTP, TCP, IP and Ethernet to different responsibilities.

## Questions
- How does encapsulation happen across TCP/IP layers?
- How do routers process IP packets while ignoring application data?

---

# Lesson 07 - Encapsulation & Decapsulation

**Date:** 2026-07-05

## What I Learned
I now understand how application data is progressively wrapped by TCP, IP and Ethernet before being transmitted as bits. I also learned why routers replace Ethernet frames while forwarding IP packets.

## Questions
- How are TCP headers interpreted by the receiving operating system?
- What happens if an IP packet is larger than the network's MTU?

---

# Lesson 08 - IP Addressing

**Date:** 2026-07-05

## What I Learned
IP addresses provide logical addressing for communication across networks, while MAC addresses are used only within a local network. I also learned why private IP addresses can be reused across millions of networks and how NAT translates them to public IP addresses for Internet communication.

## Questions
- How exactly does NAT maintain mappings for thousands of simultaneous connections?
- How does a router determine the next hop for a given destination IP address?

---

# Lesson 09

**Date:** 2026-07-06

## What I Learned
Subnets, subnet masks and CIDR.

---

# Lesson 10

**Date:** 2026-07-06

## What I Learned
ARP, ARP cache and MAC resolution.

## Lesson 11 - Routing
Completed the study of routing fundamentals including routers, default gateways, routing tables, longest prefix match, and hop-by-hop forwarding. Understood how packets move across multiple networks and why Layer 2 headers are recreated at every hop.

## Lesson 12 - Network Address Translation (NAT)
Learned why NAT was introduced to address IPv4 exhaustion, how private and public IPs interact, the roles of SNAT, DNAT, and PAT, and how routers maintain NAT tables. Also explored port forwarding, Carrier-Grade NAT, and cloud NAT Gateways.

## Lesson 13 - Domain Name System (DNS)
Learned how DNS translates domain names into IP addresses, the complete DNS resolution process, recursive and iterative queries, the DNS hierarchy, caching using TTL, and the role of common DNS record types. Also understood that DNS resolution is the first step before establishing any TCP connection or sending an HTTP request.

## Lesson 14 - Transmission Control Protocol (TCP)
Studied how TCP provides reliable communication over IP through sequence numbers, acknowledgments, retransmissions, and the Three-Way Handshake. Learned how TCP ensures ordered delivery, manages connection establishment and termination, and uses flow control and congestion control to provide efficient and reliable data transfer.

---

# Lesson 15 - User Datagram Protocol (UDP)

**Date:** 2026-08-02

## What I Learned
UDP is a connectionless transport protocol that provides low-overhead datagram delivery without TCP's guarantees of reliability, ordering and retransmission. This makes it useful for latency-sensitive applications such as gaming, real-time media and DNS. Online multiplayer battle royale games such as BGMI can use UDP for real-time gameplay traffic where low latency is more important than perfect delivery of every packet.

## Key Insight
UDP itself is unreliable, but applications can build reliability or other control mechanisms above it when required.

## Questions
- How do applications handle packet loss over UDP?
- How does QUIC provide reliable transport over UDP?

---

# Lesson 16 - How the Web Works: DNS, TCP, TLS and HTTP

**Date:** 2026-08-02

## What I Learned
I traced what happens when a URL is entered into a browser. DNS resolves the domain name, TCP establishes a connection for traditional HTTP/1.1 and HTTP/2, TLS secures HTTPS, and the browser then sends HTTP bytes through the established connection. I also learned that HTTP/3 uses QUIC over UDP.

## Key Insight
HTTP is an application-layer protocol. TCP does not understand HTTP; it transports an ordered byte stream. QUIC provides transport features over UDP and is used by HTTP/3.

## Questions
- How does TLS establish trust and encryption?
- How does QUIC handle reliability and multiplexing?

---

# Lesson 17 - HTTP Fundamentals

**Date:** 2026-08-02

## What I Learned
HTTP uses structured requests and responses containing methods, status codes, headers and optional bodies. I learned that `Accept` expresses preferred response formats while `Content-Type` describes the actual representation. I also understood why HTTP is stateless while cookies provide a mechanism for maintaining application state across requests. PUT is generally idempotent because repeating the same operation should produce the same intended final state, while POST is generally non-idempotent because repeated requests may create multiple resources or repeat an action.

## Key Insight
HTTP statelessness does not mean applications cannot maintain state. State can be implemented using cookies, sessions, tokens and server-side storage.

## Questions
- How does content negotiation work in detail?
- How do idempotency keys make POST retries safer?

---

# Lesson 18 - HTTP Request Journey Across All Layers

**Date:** 2026-08-02

## What I Learned
I traced a `GET /products/123` request from browser to server and back through DNS, TCP, TLS, HTTP, IP and the network. I learned how HTTP bytes are transported by TCP, encapsulated into IP packets, forwarded by routers and then decapsulated at the destination. The server application processes the HTTP request and may consult caches or databases before generating the response.

## Key Insight
Each networking layer has a distinct responsibility. HTTP understands application semantics, TCP provides an ordered byte stream, IP handles logical addressing and routing, and link-layer technologies deliver frames across individual network links.

## Questions
- Which information changes at every router hop?
- How do persistent HTTP connections affect the journey?

---

# Lesson 19 - Building a TCP/HTTP Server in Python

**Date:** 2026-08-02

## What I Learned
I built a minimal TCP server in Python using the socket API and then turned it into a basic HTTP server. I observed raw HTTP requests sent by curl, manually constructed HTTP responses, parsed the request line, implemented simple path-based routing and returned `200 OK` or `404 Not Found` responses.

I also learned an important limitation of the first implementation: TCP provides a byte stream, not complete HTTP messages. A single HTTP request can be split across multiple `recv()` calls, so a robust HTTP server must implement proper buffering and message parsing.

## Key Insight
The socket API is the boundary between the application and the transport layer. The operating system provides TCP bytes to the application, but the application is responsible for interpreting those bytes as HTTP.

## Questions
- How should an HTTP server buffer partial requests?
- How do headers determine the size of a request body?
- How does HTTP keep-alive allow multiple requests on one TCP connection?

---

---

# Lesson 20 - HTTP Request Parsing

**Date:** 2026-08-02

## What I Learned

I learned that TCP provides a reliable ordered byte stream rather than discrete HTTP messages. A single `recv()` call is not guaranteed to contain exactly one complete HTTP request. It may contain a partial request, one complete request, or multiple requests.

I learned how an HTTP server buffers incoming TCP bytes, finds the end of the HTTP headers using `\\r\\n\\r\\n`, parses the request line and headers, and uses `Content-Length` to determine how many bytes belong to the request body.

I also understood that a server must wait when a request is incomplete and preserve buffered bytes until enough data arrives to construct a complete HTTP request.

## Key Insight

The socket API provides TCP bytes to the application, but the HTTP server is responsible for interpreting those bytes and reconstructing HTTP message boundaries.

## Questions

- What happens when one TCP read contains multiple HTTP requests?
- How should the server preserve bytes belonging to the next request?
- How does HTTP/1.1 keep a TCP connection open for multiple requests?

---

# Lesson 21 - HTTP/1.1 Persistent Connections and Buffer Management

**Date:** 2026-08-02

## What I Learned

I learned the important distinction between HTTP statelessness and persistent TCP connections. HTTP is stateless in the sense that the protocol does not inherently require the server to remember application state between requests, while HTTP/1.1 can reuse one TCP connection for multiple independent HTTP requests and responses.

I learned that persistent connections are not permanent. They can close because of idle timeouts, `Connection: close`, server shutdown, resource limits, or network failures.

I also learned why persistent connections make request buffering especially important. One TCP `recv()` may contain multiple HTTP requests, or a complete request followed by a partial next request. The server must parse the complete request, send its response, and preserve any remaining bytes in the buffer.

The server therefore conceptually uses an outer loop to receive more TCP bytes and an inner loop to process every complete HTTP request already available in the buffer.

## Key Insight

HTTP statelessness and TCP connection persistence are independent concepts. Persistent connections are about reusing the underlying TCP connection, while statelessness is about application-level request state.

## Questions

- How does TLS fit between HTTP and TCP?
- How does the TLS handshake establish encryption and trust?
- How does HTTP/2 solve limitations of HTTP/1.1 request ordering?

---

## Lesson 25 - Inspecting HTTPS with Python

**Date:** 2026-08-29

## What I Learned

I used Python's socket and SSL APIs to make the HTTPS stack concrete. I traced the sequence from DNS resolution to TCP connection establishment, TLS handshake, certificate inspection, HTTP request transmission and HTTP response reception.

I learned that TLS does not replace HTTP or TCP. HTTP remains the application protocol, TLS provides encryption and authentication, and TCP provides a reliable ordered byte stream underneath TLS.

I also learned how Python can expose negotiated TLS information such as the TLS version, cipher and server certificate.

## Key Insight

HTTPS can be understood as HTTP transported through TLS over TCP. Observing the connection with Python makes the boundaries between HTTP, TLS and TCP much clearer.

## Questions

- How does HTTP/1.1 actually frame requests and responses over the TCP byte stream?
- How does HTTP/2 multiplex multiple streams over one connection?
- How does QUIC change the transport model used by HTTP/3?

---

# Lesson 32 - HTTP/2 Flow Control & Stream Management

**Date:** 2026-08-29

## What I Learned

I learned why HTTP/2 needs its own flow-control mechanism even though it runs over TCP. HTTP/2 has both stream-level and connection-level flow-control windows, and DATA consumes credit at both levels. The receiver can grant additional credit using `WINDOW_UPDATE` frames.

I also learned that flow control and stream management are separate from scheduling. Flow control determines how much DATA a sender is currently allowed to send, while HTTP/2 streams provide independent logical request/response lifecycles within one TCP connection.

## Key Insight

HTTP/2 flow control protects the receiver at the HTTP/2 layer, while TCP flow control and congestion control solve different problems at lower layers.

## Questions

- How should a server choose between multiple streams that are eligible to send?
- How do stream priorities interact with flow-control windows?
- Why does QUIC move stream multiplexing into the transport layer?

---

# Lesson 33 - HTTP/2 Stream Prioritization & Scheduling

**Date:** 2026-08-29

## What I Learned

I learned that HTTP/2 multiplexing creates a scheduling problem: when multiple streams are ready and allowed to send, the server must decide which stream receives transmission opportunities. HTTP/2 originally represented priorities using dependency trees and weights.

Weights provide relative scheduling preference rather than guaranteed bandwidth. Scheduling must also consider flow-control state, fairness, stream completion, TCP behavior and application goals. Pure priority scheduling can cause starvation, so production schedulers need to balance priority and fairness.

I also learned that HTTP/2's original priority model had practical limitations and that modern HTTP prioritization uses a more flexible approach.

## Key Insight

Multiplexing creates concurrency, flow control limits what can be sent, and scheduling determines how eligible streams share limited resources.

## Questions

- How does QUIC represent streams at the transport layer?
- How does QUIC avoid TCP's connection-level head-of-line blocking?
- Which TCP responsibilities must QUIC rebuild over UDP?

---

# Lesson 35 - QUIC Packets, Frames & Connection IDs

**Date:** 2026-08-29

## What I Learned

I learned how QUIC organizes transport information inside UDP datagrams. A QUIC packet contains a header and one or more frames, while frames carry specific transport operations such as STREAM data, ACKs, TLS handshake data and flow-control or connection-control information.

I learned the difference between QUIC packet numbers and stream offsets. Packet numbers are used for transport-level acknowledgments and loss detection, while stream offsets identify byte positions within individual QUIC streams. A single packet can carry frames for multiple streams.

I also learned that QUIC Connection IDs identify logical QUIC connections independently of the current network path. This enables connection migration when a client changes networks, subject to QUIC's path-validation and security mechanisms. Connection IDs and Stream IDs are separate concepts: one identifies the connection and the other identifies streams within it.

Finally, I learned the high-level distinction between QUIC's long and short packet headers and its separate packet number spaces for Initial, Handshake and Application Data traffic.

## Key Insight

The most important mental model is:

```text
QUIC connection
    |
    +-- streams
    |
    +-- packets
           |
           +-- frames
```

Packets are transport containers, frames carry protocol operations, and streams provide independent ordered byte sequences.

## Questions

- How does QUIC establish a connection and perform the TLS 1.3 handshake?
- How are QUIC packet numbers and ACK ranges used for loss detection?
- How does QUIC derive and transition between encryption keys?
- How does QUIC achieve 0-RTT and 1-RTT connection establishment?

---

# Lesson 36 - QUIC Connection Establishment & TLS 1.3

**Date:** 2026-08-29

## What I Learned

I learned how a fresh QUIC connection is established without a TCP handshake. A client can immediately send a QUIC Initial packet over UDP containing a CRYPTO frame with the TLS 1.3 ClientHello.

I learned that QUIC integrates TLS 1.3 rather than replacing it. TLS is responsible for authentication, key exchange and cryptographic secrets, while QUIC is responsible for transport reliability, acknowledgments, loss detection, streams, flow control, congestion control and connection management.

I learned the progression through Initial, Handshake and 1-RTT encryption levels. Initial packets use Initial packet-protection keys, later handshake packets use Handshake keys, and normal application traffic uses 1-RTT keys derived from the TLS handshake.

I also learned that TLS handshake messages are carried in QUIC CRYPTO frames rather than STREAM frames. If a packet carrying handshake data is lost, QUIC's loss-recovery machinery ensures that the required data is sent again in new packets.

Finally, I learned the high-level idea behind TLS 1.3 0-RTT resumption. A returning client can potentially send application data immediately, but 0-RTT data has replay considerations and therefore cannot be treated as universally safe for state-changing operations.

## Key Insight

The most important mental model is that QUIC and TLS have separate responsibilities but are tightly integrated:

```text
TLS 1.3
  -> authentication
  -> key exchange
  -> traffic secrets

QUIC
  -> packets
  -> streams
  -> reliability
  -> congestion control
  -> flow control
```

The TLS handshake supplies the cryptographic state that QUIC uses to protect its packets.

## Questions

- How exactly are TLS-derived secrets converted into QUIC packet-protection keys?
- What is AEAD and how does it authenticate QUIC packet payloads?
- How does QUIC header protection work?
- Why are QUIC packet numbers themselves protected?

---

# Lesson 37 - QUIC Packet Protection & Encryption

**Date:** 2026-08-29

## What I Learned

I learned how QUIC uses TLS 1.3-derived cryptographic material to protect packets. QUIC uses AEAD for payload protection and a separate header-protection mechanism for selected header bits and packet-number bytes.

I learned that AEAD provides both confidentiality and integrity/authentication. The QUIC payload containing frames is encrypted and authenticated as a unit, while associated data can be authenticated without being encrypted.

I learned the role of the packet-protection key, IV and header-protection key. The IV is a cryptographically derived base value that is combined with the packet number to construct the per-packet AEAD nonce. The packet number therefore makes the nonce packet-specific.

I also learned that QUIC does not necessarily transmit the complete packet number. It can transmit truncated packet-number bytes, and the receiver reconstructs the full packet number using previously received packet-number state.

Finally, I learned the high-level receive pipeline: remove header protection, recover the packet number, construct the AEAD nonce, authenticate/decrypt the payload and then process the resulting QUIC frames.

## Key Insight

The most important distinction from this lesson is:

```text
Payload protection
    -> AEAD encryption + authentication

Header protection
    -> masks selected header bits
```

Both rely on cryptographic material derived from the TLS/QUIC key schedule, but they serve different purposes.

## Questions

- How exactly is the QUIC header-protection mask generated?
- How does packet-number reconstruction choose the correct full packet number?
- How are QUIC packet-protection keys derived from TLS secrets?
- How does QUIC perform key updates during a long-lived connection?

---

# Lesson 38 - QUIC Header Protection & Packet Numbers

**Date:** 2026-08-29

## What I Learned

I learned why packet numbers are fundamental to QUIC. They are used for ACK processing, loss detection, RTT measurement and duplicate detection, and they also participate in constructing the AEAD nonce.

I learned that QUIC maintains separate packet-number spaces for different encryption levels, rather than using one global packet-number counter across the entire connection.

I learned that QUIC uses header protection to mask selected bits of the packet header, including the packet-number bytes. Header protection is separate from AEAD payload protection. A header-protection key and a ciphertext sample are used to generate the mask.

I learned that QUIC can transmit a truncated packet number to reduce packet overhead. The receiver reconstructs the full packet number using the packet-number state it already has and the packet-number decoding rules.

I also connected packet-number reconstruction back to packet protection: once the full packet number is recovered, QUIC combines it with the IV to construct the AEAD nonce and can then authenticate and decrypt the packet payload.

## Key Insight

The most important mental model from this lesson is:

```text
Protected packet
      |
      v
Remove header protection
      |
      v
Recover packet number
      |
      v
IV + Packet Number
      |
      v
AEAD nonce
      |
      v
Authenticate + decrypt
```

Header protection and AEAD are complementary mechanisms, not interchangeable ones.

## Questions

- How does QUIC detect a lost packet?
- How do ACK ranges communicate received packets efficiently?
- When does QUIC decide that a packet is lost?
- How does QUIC retransmit data without retransmitting the original packet itself?

---

# Lesson 39 - QUIC Reliability, Loss Detection & ACKs

**Date:** 2026-08-29

## What I Learned

I learned how QUIC builds reliable transport behavior above UDP using packet numbers, ACK frames, ACK ranges, RTT measurements and loss detection. A missing packet is not immediately considered lost because it may simply be delayed.

I learned that QUIC uses both packet-number evidence and time-based evidence to decide when a packet is likely lost. RTT estimation is therefore an important part of the transport system.

I also learned an important distinction between packet retransmission and data retransmission. QUIC does not generally retransmit the original packet identity. Instead, reliable data from a lost packet is placed into a new packet with a new packet number.

## Key Insight

The core reliability loop is:

```text
Packet Numbers
      |
      v
ACK Frames
      |
      v
Loss Detection
      |
      v
Lost Data
      |
      v
New Packet
      |
      v
Retransmitted Data
```

## Questions

- How does QUIC decide exactly when a packet is lost?
- How does congestion control react to packet loss?
- How do QUIC streams interact with retransmitted data?

---

# Lesson 40 - QUIC Streams & Multiplexing

**Date:** 2026-08-29

## What I Learned

I learned that a QUIC connection can contain many independent streams, each represented as an ordered byte sequence. STREAM frames identify the stream and the byte offset where their data belongs.

I learned the difference between packet numbers and stream offsets. Packet numbers identify transport packets and support ACK/loss processing, while stream offsets reconstruct ordered application data within an individual stream.

I learned that QUIC supports bidirectional and unidirectional streams and that multiple streams can be multiplexed over one QUIC connection.

Most importantly, I understood why QUIC avoids TCP's connection-level head-of-line blocking. If data for Stream 4 is missing, Stream 4 may wait for its missing bytes, but unrelated Stream 8 data can continue when available. This does not mean streams are completely independent: they still share congestion-control capacity, connection-level flow control and the underlying connection.

## Key Insight

The fundamental architecture is:

```text
QUIC Connection
      |
      +--- Stream 4
      +--- Stream 8
      +--- Stream 12
```

Each stream has its own ordering, while packets provide the transport container used to carry stream data.

## Questions

- How does QUIC control how much data each stream can send?
- How does connection-level flow control interact with stream-level flow control?
- How does congestion control differ from flow control?

---

# Lesson 41 - QUIC Flow Control & Congestion Control

**Date:** 2026-08-29

## What I Learned

I learned that QUIC has two different reasons for limiting how much data can be sent. Flow control protects the receiver, while congestion control protects the network.

QUIC flow control exists at two levels: stream-level flow control using `MAX_STREAM_DATA`, and connection-level flow control using `MAX_DATA`. The receiver can increase these limits as it consumes data.

I also learned about the congestion window (`cwnd`), which limits how much congestion-controlled data can be outstanding in the network. This is independent of the receiver's flow-control capacity.

## Key Insight

The sender is constrained by multiple limits. Conceptually:

```text
Actual send capacity
≈ min(
    stream flow-control capacity,
    connection flow-control capacity,
    congestion-control capacity
)
```

## Questions

- How does QUIC choose its congestion-control algorithm?
- How do ACKs and loss detection influence congestion-window changes?
- How are stream and connection flow-control windows chosen in real implementations?

---

# Lesson 42 - QUIC Connection Migration & Final Architecture

**Date:** 2026-08-29

## What I Learned

I learned why a traditional TCP connection can be disrupted when a device changes its IP address or network path. QUIC separates logical connection identity from network location using Connection IDs.

I learned that QUIC can support connection migration, allowing a logical connection to continue over a new network path. I also learned about NAT rebinding, where a NAT can change the apparent external UDP port even without a deliberate network switch.

New paths cannot simply be trusted. QUIC uses path validation mechanisms such as `PATH_CHALLENGE` and `PATH_RESPONSE` to establish that the new path is usable by the peer.

Finally, I consolidated the QUIC architecture: streams and multiplexing, packet numbers and ACKs, reliability and loss detection, TLS and packet protection, flow control, congestion control, Connection IDs, path validation and migration all operate together underneath HTTP/3.

## Key Insight

The most important architectural distinction is:

```text
IP address
    |
    v
Where the endpoint currently is

Connection ID
    |
    v
Which logical QUIC connection this belongs to
```

This separation is what enables QUIC to be resilient to supported network-path changes.

## Questions

- How exactly does HTTP/3 map requests and responses onto QUIC streams?
- What HTTP/2 concepts disappear when HTTP is mapped directly onto QUIC?
- How are HTTP/3 control and request streams structured?

---
