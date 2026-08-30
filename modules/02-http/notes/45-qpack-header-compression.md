# Lesson 45 — QPACK: HTTP/3 Header Compression

## 1. Why Header Compression?

HTTP requests and responses repeatedly contain the same headers:

```text
:method: GET
:scheme: https
accept-encoding: gzip, br
user-agent: ...
```

Sending these headers in full for every request wastes bandwidth.

HTTP/2 uses HPACK. HTTP/3 uses QPACK.

```text
HTTP/2 -> HPACK
HTTP/3 -> QPACK
```

## 2. Header Tables

QPACK uses indexed representations so common headers can be represented compactly.

There are two important tables:

```text
QPACK
  |
  +---- Static Table
  |
  +---- Dynamic Table
```

## 3. Static Table

The QPACK static table is a predefined table specified by the QPACK specification.

Both endpoints already know its contents.

Conceptually:

```text
Static Table

Index    Header
---------------------------
  ...    :method: GET
  ...    :scheme: https
  ...    :path: /
  ...    ...
```

The static table is **not updated during a connection**.

This is the key distinction:

> Static means fixed by the protocol specification, not "updated infrequently."

No synchronization is required to create or modify the static table during a connection because both endpoints already have the same predefined table.

## 4. Dynamic Table

The dynamic table contains entries created during communication.

For example:

```text
cookie: session=abc123
```

can be inserted into the dynamic table and later referenced by index.

Conceptually:

```text
Dynamic Table

Entry 1 -> cookie: session=abc123
Entry 2 -> custom-header: value
```

Dynamic table state is connection-specific and changes during the connection.

## 5. Static vs Dynamic

```text
STATIC TABLE
------------------------------
Defined by QPACK specification
Known beforehand
Does not change during connection
No synchronization required

DYNAMIC TABLE
------------------------------
Maintained during connection
Entries can be inserted/evicted
Requires synchronization
Uses QPACK encoder/decoder streams
```

The difference is therefore not frequency of change. The static table is immutable for a given QPACK specification/version, while the dynamic table is mutable connection state.

## 6. Why Static Entries Are Useful

Common headers can be referenced immediately.

Instead of sending:

```text
:method: GET
```

QPACK can use the corresponding static-table index.

```text
Request
   |
   v
Static table reference
   |
   v
Header reconstructed by decoder
```

No dynamic-table insertion or synchronization is necessary.

## 7. Why QPACK Was Needed Instead of Simply Reusing HPACK

HTTP/2's HPACK operates over HTTP/2 streams carried through a single ordered TCP byte stream.

```text
HTTP/2 streams
      |
      v
    HPACK
      |
      v
     TCP
```

Dynamic compression state can create dependencies between header blocks.

With HTTP/3, QUIC provides independently progressing streams:

```text
HTTP/3 request streams
      |
      v
     QPACK
      |
      +---- Encoder Stream
      |
      +---- Decoder Stream
      |
      v
     QUIC
```

QPACK is designed so header compression does not blindly recreate global transport-level head-of-line blocking.

## 8. QPACK Streams

QPACK uses two dedicated unidirectional QUIC streams.

The encoder stream carries encoder instructions toward the decoder:

```text
Encoder --------------------> Decoder
          Encoder Stream
```

The decoder stream carries decoder instructions and acknowledgments in the opposite direction:

```text
Decoder --------------------> Encoder
          Decoder Stream
```

## 9. Dynamic Table Insertion

Suppose the encoder wants to add:

```text
cookie: session=abc123
```

to the dynamic table.

Conceptually:

```text
Client                         Server

QPACK Encoder Stream
      |
      | INSERT cookie: session=abc123
      |------------------------------>
      |                               |
      |                         Dynamic Table
      |                         +----------------+
      |                         | cookie: ...    |
      |                         +----------------+
```

A later header block can reference the dynamic entry instead of repeating the entire header.

## 10. Dynamic Dependencies and Blocked Streams

A request header block may depend on a dynamic table entry that the decoder has not processed yet.

For example:

```text
Dynamic insert count = 47
Required insert count = 50
```

The decoder cannot decode that header block until the required dynamic entries are available.

Therefore one request stream may temporarily block:

```text
Stream 4 -> waiting for dynamic table state
```

while another stream can continue:

```text
Stream 8 -> continues
Stream 12 -> continues
```

This is different from transport-level TCP head-of-line blocking, where missing bytes could hold up everything behind them in the single TCP byte stream.

## 11. QPACK Does Not Make Every Dependency Disappear

QUIC provides independent transport streams, but application-level protocols can still introduce dependencies.

Therefore:

> QUIC removes transport-level head-of-line blocking between streams; it does not eliminate every possible application-level dependency.

QPACK manages these dependencies explicitly.

## 12. QPACK and HTTP/3 HEADERS

HTTP/3 HEADERS frames contain compressed header blocks.

Conceptually:

```text
HTTP/3 HEADERS
       |
       v
     QPACK
       |
       v
compressed header block
       |
       v
QUIC request stream
```

The QUIC layer does not understand the meaning of the compressed header block. It transports the bytes belonging to the QUIC stream.

## 13. Static Table Does Not Get Dynamically Updated

This distinction is especially important:

```text
Static Table
     |
     +---- fixed by QPACK specification
     +---- known by implementations
     +---- unchanged during connection

Dynamic Table
     |
     +---- populated during connection
     +---- modified during connection
     +---- connection-specific
     +---- synchronized through QPACK mechanisms
```

If a future QPACK specification defines a different static table, that is a change in the protocol specification/implementation, not an update to an existing connection's static table.

## 14. Complete Mental Model

```text
                         HTTP/3
                            |
                  +---------+---------+
                  |                   |
               HEADERS               DATA
                  |
                QPACK
                  |
        +---------+---------+
        |                   |
   Static Table        Dynamic Table
        |                   ^
        |                   |
        |            Encoder Stream
        |                   |
        +---------+---------+
                  |
                 QUIC
                  |
             Request Stream
                  |
               QUIC packets
                  |
                 UDP
```

## 15. Key Takeaways

1. HTTP/3 uses QPACK for header compression.
2. QPACK has a predefined static table and a mutable dynamic table.
3. The static table does not get updated during a connection.
4. The dynamic table changes during a connection and requires synchronization.
5. QPACK uses dedicated encoder and decoder unidirectional streams.
6. Dynamic-table dependencies can temporarily block an individual request stream.
7. Such blocking is different from TCP's transport-level head-of-line blocking.
8. QPACK is designed around QUIC's independently progressing streams.
