# Lesson 14: Transmission Control Protocol (TCP)

## Concepts Covered
- Purpose of TCP
- Best-effort delivery in IP
- Reliable communication using TCP
- TCP segments
- Sequence numbers
- Acknowledgments (ACKs)
- Three-Way Handshake
- Connection termination
- Retransmissions
- Flow Control
- Congestion Control
- TCP ports

## Key Learnings
- IP provides best-effort packet delivery, while TCP provides reliable, ordered, and error-checked communication.
- TCP establishes a connection using the Three-Way Handshake before exchanging application data.
- Sequence numbers allow the receiver to detect missing or out-of-order data.
- Acknowledgments confirm successful receipt of data, enabling retransmission of lost segments.
- Flow control prevents overwhelming the receiver, while congestion control prevents overloading the network.
- TCP is used by many application protocols including HTTP, HTTPS, SSH, SMTP, and FTP.

## Important Terms
- TCP
- Segment
- Sequence Number
- ACK
- SYN
- FIN
- Three-Way Handshake
- Retransmission
- Flow Control
- Congestion Control
- Port

## Real-world Applications
- Web browsing (HTTP/HTTPS)
- File transfers
- Email
- Remote login (SSH)
- Database connections
- Reliable API communication

## Next Lesson
User Datagram Protocol (UDP)