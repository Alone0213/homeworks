# Research and Analysis of OPSA: An Efficient and Verifiable One-Pass Secure Aggregation Protocol Based on TEE

**Abstract:** Federated Learning (FL), as a decentralized collaborative machine learning paradigm, enables multi-party cooperative model training while preserving data privacy. Model updates may leak original private data during the process. Secure Aggregation (SA) protocols are widely used to protect user privacy during model aggregation. Existing SA protocols require at least three rounds of communication per aggregation and lack mechanisms for verifying aggregation results. Verifiable SA can compensate for verification deficiencies but incurs high communication costs. SA schemes based on Trusted Execution Environment (TEE) can reduce round trips but face computational bottlenecks due to TEE's limited physical memory. This paper conducts an in-depth analysis of OPSA—an efficient and verifiable one-pass SA protocol based on TEE. OPSA handles client dropout through server-side TEE, enabling the server to complete masked model aggregation in a single pass, significantly reducing communication rounds. To mitigate TEE limitations, OPSA offloads model aggregation and mask elimination tasks outside the TEE, handling only shared keys inside the TEE. This paper proposes KhPRF-OPSA (single-layer masking) and POT-OPSA (double-layer masking) protocols, both employing novel cryptographic primitives. OPSA integrates commitment and signature mechanisms, requiring only O(1) additional communication overhead per client to ensure result verifiability. Compared with existing state-of-the-art schemes, OPSA achieves 2 to 10 times speed improvement across multiple aggregation rounds while ensuring result verifiability. This paper builds upon the original OPSA paper, combining course knowledge of cryptography and network security to conduct an extended analysis and evaluation of the OPSA protocol.

**Keywords:** Federated Learning; Secure Aggregation; Verifiable Aggregation; Trusted Execution Environment; Privacy Protection

## I. Research Background and Significance

### 1.1 Development of Federated Learning and Privacy Challenges

With the rapid development of big data and artificial intelligence technologies, the demand for data in machine learning model training continues to grow. Traditional centralized training methods require aggregating data scattered across various institutions and devices to a central server, which creates enormous communication bandwidth pressure and raises severe data privacy and security concerns[1]. To address this challenge, McMahan et al. proposed the concept of Federated Learning (FL) in 2017[2]. The core idea is to train models locally on participating devices without moving raw data, uploading only model updates (gradients or weights) to the central server for aggregation, enabling multi-party collaborative model training.

The paradigm shift of federated learning has revolutionary significance: raw data remains on local devices, fundamentally reducing the risk of data leakage. Communication overhead shifts from transmitting raw datasets to transmitting model parameters, significantly reducing bandwidth requirements. Federated learning enables cross-institutional collaboration in highly sensitive domains such as healthcare and finance. As research progresses, researchers have discovered that federated learning is not absolutely secure. The Deep Leakage from Gradients attack proposed by Zhu et al.[3] demonstrates that attackers can reconstruct users' original training data from shared gradient information. Model Inversion Attacks proposed by Fredrikson et al.[4] also prove that sensitive attributes in training data can be inferred by analyzing model outputs. These findings reveal the vulnerability of privacy protection in federated learning, highlighting the necessity of implementing stronger privacy protection measures during model aggregation.

### 1.2 Evolution of Secure Aggregation Technology

To protect user privacy during model aggregation, Secure Aggregation (SA) technology emerged. The core idea of SA requires each client to mask its local model in a specific way. The server aggregates these masked models to recover the plaintext global model without learning any individual client's true model updates[5].

In 2017, Bonawitz et al. proposed the first practical secure aggregation protocol (SecAgg)[5]. This protocol uses secret sharing and pairwise masking techniques to ensure the global model can still be successfully recovered even when some clients drop out. Bell et al.[6] upgraded it to SecAgg+, enhancing robustness against malicious clients. These schemes are more suitable for single-round federated learning scenarios because each aggregation requires clients to regenerate and share keys, significantly increasing communication overhead.

To support multi-round aggregation scenarios, MicroFedML[7] achieves key reuse through a one-time setup phase. Flamingo[8] designed a multi-round secure aggregation protocol using pairwise masking, while LERNA[9] achieved the same goal through a single masking mechanism. Although these schemes achieve reusable setup phases by introducing additional groups, each aggregation still requires three rounds of client-server communication (as shown in Figure 1), which presents clear limitations in high-latency or bandwidth-constrained environments.

The decrypter group in Flamingo and the committee in LERNA can both be viewed as trusted entities. Researchers began to explore: can hardware-based Trusted Execution Environments (TEE) replace these special groups, achieving communication-optimized aggregation while maintaining TEE internal computing efficiency?

### 1.3 OPSA Research Motivation and Core Contributions

Executing SA operations entirely within a TEE environment can optimize the communication round-trip process. TEE's limited physical memory introduces significant computational bottlenecks, particularly when aggregating large models or handling numerous clients. A global model with one million parameters requires approximately 3.8 MB of memory (4 bytes per parameter). In scenarios involving hundreds of clients, memory requirements easily exceed the 128 MB physical memory capacity of TEE.

To address this problem, Guan et al.[10] proposed the OPSA (One-Pass Secure Aggregation) protocol. Its core contributions can be summarized in three aspects: they proposed an efficient and verifiable multi-round single-pass SA framework based on TEE. With TEE assistance, the server completes masked model aggregation in a single pass, significantly reducing communication round trips. TEE handles only key processing operations, and its memory consumption is independent of model scale, effectively alleviating computational bottlenecks. They designed KhPRF-OPSA (single-layer masking protocol based on key-homomorphic pseudo-random functions) and POT-OPSA (double-layer masking protocol based on proxy oblivious transfer), both employing innovative cryptographic primitives. They integrated commitment and signature mechanisms, requiring only constant-factor additional communication overhead per client to ensure result verifiability.

The significance of this research: OPSA represents a major breakthrough in communication efficiency for secure aggregation technology. Through the innovative combination of TEE technology and cryptographic primitives, it provides new approaches to balancing privacy protection and efficiency in federated learning. In-depth analysis and understanding of the OPSA protocol hold important theoretical and practical value for advancing secure aggregation technology.

## II. Theoretical Foundation and Security Assumptions

### 2.1 Federated Learning and Secure Aggregation Fundamentals

A typical federated learning scenario involves n clients and one server. In the formal definition, each client u holds a private dataset D_u, and the server holds the initial global model parameters θ^(0). For each training round r ∈ [1,R], participants repeat the following process until the global model θ converges: the server broadcasts the current global model θ^(r-1) to all participating clients. Each client u ∈ U receives the updated global model θ^(r-1) from the previous round and combines it with its private dataset to train a local model x_u^(r) = θ^(r-1) - η · ∇L_u(θ^(r-1)), where η is the learning rate and ∇L_u is the loss function gradient of client u on local data. The server collects individual models x_u^(r) from different clients and computes the aggregated model z^(r) = Σ_{u∈V} x_u^(r) to update the global model θ^(r) and pass it to clients for the next training round. Clients may drop out of federated learning training at any step, with dropout rates potentially reaching over 30% of total participating clients, placing high demands on dropout resilience mechanisms.

From a cryptographic perspective, the model update process in federated learning is essentially a Secure Multi-Party Computation (MPC) process. Secure aggregation, as a special case of MPC, aims to compute the sum of all inputs without revealing any individual party's private input. Unlike traditional MPC, secure aggregation in federated learning has the following characteristics: large number of participants (up to millions), high model dimensionality (up to millions of parameters), unstable network communication (frequent mobile device dropout), and heterogeneous computational resources (significant variations in device computing power). These characteristics cause severe performance bottlenecks when general MPC protocols are directly applied to federated learning, requiring specially designed efficient secure aggregation protocols.

The core idea of Secure Aggregation (SA) is to protect the confidentiality of individual model updates through cryptographic means. Before sending its model update x_u, each client u generates a mask mask_u and sends y_u = x_u + mask_u to the server. After collecting masked models from all clients, the server computes Σ_{u∈V} y_u and uses the cancellation relationship between masks to recover Σ_{u∈V} x_u. To address client dropout, SA protocols also introduce secret sharing mechanisms, ensuring the server can correctly remove masks of dropped clients even when some clients exit. The core idea of secret sharing splits each client's mask key into multiple shares distributed to other clients for safekeeping. When recovering the mask of a dropped client, collecting shares from a sufficient number of other clients reconstructs the mask key.

### 2.2 Trusted Execution Environment (TEE) Technology

A Trusted Execution Environment (TEE) is a hardware-level security solution, with typical implementations including Intel Software Guard Extensions (SGX) and ARM TrustZone[11]. TEE creates an isolated secure area called an "Enclave" within the processor, ensuring the confidentiality and integrity of code and data executed within it. Even if privileged software such as the operating system or hypervisor is compromised, data inside the enclave cannot be accessed.

Core security properties provided by TEE include: isolated execution, ensuring computations within the enclave are free from external software interference; memory encryption, protecting data confidentiality within the enclave; and Remote Attestation, allowing remote users to verify the authenticity of applications and hardware platforms running in the enclave[12]. These properties make TEE an ideal choice for building a Trusted Computing Base (TCB) and serve as the key supporting technology enabling OPSA to achieve secure aggregation with single-pass communication.

TEE also has inherent limitations: its physical memory capacity is limited (e.g., Intel SGX enclave memory上限约128MB), and data exchange with the external environment requires memory encryption operations with significant performance overhead. These limitations are fully considered in OPSA's design.

### 2.3 Cryptographic Primitives

OPSA protocol implementation relies on multiple cryptographic primitives, including the following:

A Pseudo-Random Function (PRF)[13] is a deterministic function that, given a random seed and input value, produces an output computationally indistinguishable from truly random numbers. In OPSA, PRFs generate mask keys and random numbers.

A Key-Homomorphic PRF (KhPRF)[14] is a special class of PRF satisfying the additive homomorphic property: given two different keys k1 and k2, for any input x, PRF(k1,x) + PRF(k2,x) = PRF(k1+k2,x). This property is the mathematical foundation enabling KhPRF-OPSA to achieve efficient single-layer mask aggregation.

The Vector Pedersen Commitment scheme[15] allows a committer to commit to a vector and later open the commitment to verify its original value. The scheme satisfies two core properties: Hiding, meaning the commitment value does not reveal any information about the committed vector; and Binding, meaning the committer cannot open the same commitment to different vector values.

Digital signature schemes provide message source authentication and integrity protection. In OPSA's result verification mechanism, TEE instances and clients respectively use signature schemes to sign commitment values, ensuring the authenticity and non-repudiation of aggregation results.

Oblivious Transfer (OT) and its variant Proxy Oblivious Transfer (POT)[16] are foundational components of the POT-OPSA protocol. POT involves three parties (sender, chooser, and proxy). The sender holds two inputs, the chooser obtains one correct value based on its choice bit, and the proxy learns nothing about either the choice bit or the transferred value during the assistance process.

### 2.4 Security Model and Assumptions

The OPSA protocol is analyzed based on the following security model and assumptions:

In terms of network model, the protocol assumes authenticated channels between clients and the server, ensuring the authenticity of communicating parties' identities. It also assumes P2P secure channels between the server and all clients for key agreement and other operations.

In terms of adversary model, OPSA considers two types of adversaries: semi-honest adversaries, who honestly execute the protocol but may attempt to extract additional information from the protocol execution; and malicious adversaries, who may arbitrarily deviate from protocol specifications to undermine security. OPSA's security proof operates under a combined model of semi-honest clients and malicious servers. Clients may be semi-honest (attempting to obtain other clients' information while following the protocol), while the server may be malicious (capable of tampering with aggregation results).

In terms of security assumptions, OPSA's security depends on: the Decisional Diffie-Hellman (DDH) assumption and its variant, the 2-Oracle Diffie-Hellman (2ODH) assumption; the security assumption of pseudo-random functions; existential unforgeability under chosen-message attacks (EUF-CMA) for digital signature schemes; and the hiding and binding assumptions of commitment schemes.

TEE's own security assumptions are also an important component of OPSA's security model. The protocol assumes TEE provides a secure isolated execution environment and that remote attestation mechanisms enable users to verify the correctness of programs running in the TEE.

## III. Protocol Design

### 3.1 OPSA Overall Architecture Design

The overall design philosophy of OPSA: handling client dropout through server-side TEE mechanisms enables the server to complete masked model aggregation in a single pass. OPSA divides system roles into three categories: multiple clients participating in federated learning, a central server performing aggregation operations, and a trusted TEE instance deployed on the server side.

OPSA protocol execution has two phases: the One-time Setup Phase and the Training Phase. During the one-time setup phase, each client u establishes a shared key ku,e = KA(sku, pke) with the TEE instance Me through a key agreement protocol, where KA represents a non-interactive key agreement protocol. During this phase, clients also establish pairwise shared keys ku,v = KA(sku, pkv) between each other, used for the double-layer masking in POT-OPSA.

In each round r of the training phase, the process proceeds as follows: each client u computes a mask mask_u using the key shared with TEE instance Me and sends the masked model y_u = x_u + mask_u to the server. The server identifies the set of surviving clients V and the set of dropped clients D, passing this information to the TEE instance Me. The TEE instance recovers the aggregate mask mask_V for the server based on the key information of dropped clients. The server uses the aggregate mask to remove masks from the sum of masked models of all surviving clients, recovering the aggregate model Σ_{u∈V} x_u.

The key advantage of this design: TEE handles only key operations (key recovery and aggregate mask computation), with memory consumption related only to the number of clients, independent of model scale, effectively avoiding the computational bottlenecks caused by TEE's limited physical memory. Computation-intensive tasks such as model aggregation and mask elimination are completed on the server outside the TEE, fully utilizing the server's computational resources.

### 3.2 KhPRF-OPSA Single-Layer Masking Protocol

KhPRF-OPSA is a single-layer masking secure aggregation protocol built on Key-Homomorphic PRFs (KhPRF). The core idea leverages the additive homomorphic property of KhPRF, allowing masks generated by multiple clients to automatically cancel out after aggregation, requiring only a single masking operation.

In KhPRF-OPSA, each client u computes the mask as:
mask_u = KF(F_1(k_u,e, r), b)

F_1 is a secure pseudo-random function operating on round r and the shared key ku,e between client u and TEE instance Me. KF is a 1-almost key-homomorphic PRF operating on temporary key k_u' = F_1(ku,e, r) and public parameter b.

For the set of surviving clients V^(r), the TEE computes the aggregate temporary key k_V^(r) = Σ_{u∈V^(r)} F_1(k_e,u, r). Due to the almost key-homomorphic property of KhPRF, the server can compute the aggregate mask as KF(k_V^(r), b) + e, where |e_i| < ε for all i ∈ [1,m]. The aggregate model can be recovered as:
Σ_{u∈V^(r)} x_u^(r) = (1/|V|) · [Σ_{u∈V^(r)} y_u - KF(k_V^(r), b)]

The error e produced during aggregation in this protocol is very small and can be eliminated through rounding operations to obtain precise aggregation results. KhPRF-OPSA's advantage lies in extremely low communication overhead: each client sends only one masked model per round, and the TEE internally only needs to handle key aggregation operations.

### 3.3 POT-OPSA Double-Layer Masking Protocol

POT-OPSA is a double-layer masking secure aggregation protocol built on Proxy Oblivious Transfer (POT). Unlike KhPRF-OPSA, POT-OPSA employs a double-layer masking mechanism, simultaneously using individual keys and pairwise keys to protect client models, providing stronger security guarantees.

In POT-OPSA, each client u computes the mask as:
mask_u = G(ku_e) + Σ_{v∈U, u<v} G(F_0(k_u,v, r)) - Σ_{v∈U, u>v} G(F_0(k_u,v, r))

F_0 is a secure pseudo-random function operating on round r. G is a secure pseudo-random generator operating on the temporary individual key ku_e or temporary pairwise key k_u,v = F_0(k_u,v, r). When r ∈ [1,R], the key k_u,v is shared between client u and its neighbor v.

To safely and efficiently handle client dropout, POT-OPSA introduces the Proxy Oblivious Transfer protocol (POTkn), involving three parties: sender, chooser, and proxy. The sender knows two inputs m0 and m1. The chooser obtains mb based on its choice bit b. The proxy learns no information during the assistance process. In the OPSA context, the POT protocol transfers key information of dropped clients securely: the TEE acts as the sender, the chooser (server) obtains the required keys based on specific choice bits, and the proxy (TEE instance) reveals no additional information during assistance.

POT-OPSA's advantage lies in providing stronger privacy protection, ensuring confidentiality of individual model updates even when facing more powerful attack models. The trade-off is slightly increased communication and computational overhead compared to KhPRF-OPSA.

### 3.4 Result Verification Mechanism Design

Existing secure aggregation protocols generally lack mechanisms for verifying final aggregation results, making aggregation results vulnerable to tampering by malicious servers. OPSA integrates commitment and signature mechanisms to design a lightweight result verification scheme.

In each training round of KhPRF-OPSA or POT-OPSA, each surviving client u sends a commitment to the original model com_u = Commit(x_u, rand_u), where rand_u is a random number, along with the masked model. Each client signs the commitment value σ_u = Sign(sk_u, com_u). The TEE instance Me collects commitments from all surviving clients, computes the aggregate commitment com = Π_{u∈V} com_u and aggregate random number rand = Σ_{u∈V} rand_u, then signs the aggregate commitment and random number σ_e = Sign(sk_e, com||rand||r).

After aggregation completes, the server sends the aggregation result (x_r, com, rand, σ_e) to all clients. Clients can verify the correctness of the aggregation result by checking: (1) whether σ_e is a valid signature from the TEE instance for (com||rand||r); (2) whether Commit(x_r, rand) = com holds. If both verifications pass, clients can be confident that the aggregation result is authentic and untampered.

The security of this verification mechanism relies on the binding property of commitment schemes, the EUF-CMA security of digital signature schemes, and the remote attestation mechanism of TEE. Even if the server is malicious, it cannot forge valid commitment-signature pairs, ensuring aggregation result verifiability. This verification mechanism requires only O(1) additional communication overhead per client, not becoming a system performance bottleneck.

## IV. Security Analysis

### 4.1 Privacy Protection Security Analysis

The privacy protection goal of OPSA is to avoid leaking any individual client's model update information during aggregation. In KhPRF-OPSA and POT-OPSA protocols, each client sends a masked model y_u = x_u + mask_u to the server. Since the mask mask_u is generated by a secure pseudo-random function using a key shared between the client and TEE instance, the server cannot extract x_u from y_u without TEE assistance. From an information-theoretic perspective, the empirical distribution of y_u is indistinguishable from a uniformly random vector distribution, so the server's posterior information about x_u does not exceed its prior information.

In POT-OPSA, due to the double-layer masking mechanism (using both individual keys and pairwise keys), even if multiple clients collude, they cannot break the mask of honest clients. Pairwise masks are shared only between two clients, with no other party knowing the key. The double-layer mask structure of POT-OPSA includes two layers of protection: the first layer uses an individual key ku_e to generate the mask component G(ku_e), known only to client u and TEE instance Me; the second layer uses a set of mask components generated with pairwise keys k_u,v, each shared only between paired clients. This layered design requires attackers to break multiple security assumptions simultaneously to recover a single client's model update.

In KhPRF-OPSA, single-layer masking security depends on the security of KhPRF and key confidentiality. The almost key-homomorphic property of KhPRF enables efficient aggregate mask computation but also means all surviving clients share the same aggregate key kV^(r), requiring the TEE instance to honestly execute the protocol. If the TEE instance is compromised, attackers could directly obtain kV^(r) and recover all surviving clients' aggregate model.

OPSA's security model assumes clients are semi-honest (following the protocol but potentially attempting to obtain additional information), while the behavior of the server and TEE instance faces stricter security analysis. Under the semi-honest client assumption, OPSA protocol security is reducible to the security of underlying cryptographic primitives. OPSA's security model assumes TEE is trusted, directly related to the actual level of TEE hardware security guarantees. Side-channel attacks against SGX in recent years (such as Plundervolt, Cache Side-Channel, etc.) indicate that TEE's physical security is not absolute, requiring comprehensive evaluation combined with physical security measures.

### 4.2 Dropout Resilience Security Analysis

Client dropout is a common phenomenon in federated learning. Secure aggregation protocols must handle client dropout without affecting aggregation correctness. OPSA achieves efficient dropout-resilient aggregation by using TEE to handle key recovery of dropped clients.

In KhPRF-OPSA, when client v drops out in round r, the TEE instance Me has stored the shared key ke,v = KA(ske, pkv) with client v. TEE uses these keys to recompute the mask component of the dropped client and incorporates it into the aggregate mask computation, ensuring the dropped client's mask does not affect the correctness of the final aggregation result.

In POT-OPSA, the TEE instance recovers both the individual key component ke,v and pairwise key components {ke,v,u} (for pairwise masks with other surviving clients) of dropped clients. By incorporating these key components into the aggregate mask computation, the server correctly removes all masks introduced by dropped clients.

OPSA's dropout resilience satisfies: when the number of surviving clients |V| ≥ ⌈(1-δ)N⌉ and (1-δ) ≥ α (where α is the minimum survival ratio of the sum ideal functionality defined in Definition 4), aggregation completes successfully. This condition ensures OPSA operates normally under reasonable client dropout ratios.

### 4.3 Result Authenticity and Integrity Analysis

OPSA's result verification mechanism protects against two types of tampering by malicious servers. A malicious server A attempting to output a tampered global model z_A = z_H + x̃_A + e (where z_H is the true aggregation result of honest surviving clients, x̃_A is a tampered individual model, and e is an introduced error vector) could be accepted by semi-honest clients in two scenarios:

The first scenario: the server can generate z_A based on the same com and rand. This requires the server to find an x' such that Commit(x', rand) = com, directly violating the binding property of the Vector Pedersen Commitment scheme and is computationally infeasible.

The second scenario: the server can forge the TEE instance Me's signature for a new commitment com' and random number rand'. This requires the attacker to generate a valid signature without knowing the signing private key ske, violating the security assumptions of the EUF-CMA secure signature scheme.

Under the binding property assumption of commitment schemes and the EUF-CMA security assumption of signature schemes, OPSA's result verification mechanism effectively detects tampering by malicious servers, ensuring the authenticity and integrity of aggregation results.

### 4.4 Hybrid Security Proof Framework

OPSA's security is proven using the standard Hybrid Argument method. The proof progressively reduces the actual protocol execution to the ideal function's secure simulation through a series of indistinguishable hybrid experiments.

Taking KhPRF-OPSA as an example, the security proof completes through the following hybrid steps: Hyb0 is the joint view of all participants in the actual protocol execution. Hyb1 has the simulator mastering all honest participants' secret information and simulating protocol execution. Hyb2 replaces shared keys between clients and TEE with random keys (based on the 2ODH assumption). Hyb3 replaces masked models sent by clients with uniformly random sampled values (based on statistical indistinguishability of masks). Hyb4 replaces keys and aggregate masks output by TEE with simulated values (based on the hiding property of commitment schemes and the security of signature schemes). Hyb5 sets the output of the ideal functionality to the true aggregated model.

Through these five hybrid steps, the adversary's joint view in actual execution is computationally indistinguishable from the simulator's output, proving OPSA protocol security under the malicious server model. A similar proof framework applies to the POT-OPSA protocol, with the difference requiring additional handling of secure replacement of pairwise keys.

## V. Comparative Analysis and Applications

### 5.1 Communication Efficiency Comparison with Existing Schemes

OPSA demonstrates significant advantages in communication efficiency compared to existing schemes. Traditional secure aggregation protocols (such as SecAgg and SecAgg+) require at least three rounds of client-server communication per aggregation: the first round for broadcasting public keys, the second for sending masked models and secret sharing shares, and the third for sending mask keys. Even optimized multi-round schemes (such as Flamingo and LERNA) maintain this communication pattern. Table 1 summarizes the differences in communication rounds among various schemes.

**Table 1: Communication Round Comparison**

| Scheme | Setup Phase | Communication Rounds/Round | Verifiable | TEE Required |
|--------|-------------|---------------------------|------------|--------------|
| SecAgg | N/A | 3 rounds | No | No |
| SecAgg+ | N/A | 3 rounds | No | No |
| Flamingo | 1 setup | 3 rounds | No | No |
| LERNA | 1 setup | 3 rounds | No | No |
| KhPRF-OPSA | 1 setup | 1 round | Yes | Yes |
| POT-OPSA | 1 setup | 1 round | Yes | Yes |

OPSA reduces the required communication rounds to a single round trip by using server-side TEE to handle client dropout. In KhPRF-OPSA, clients only need to send one masked model per training round (along with commitment and signature), and the server completes aggregation and returns results with TEE assistance. This single-round communication mode has particularly significant advantages when processing large models or in high-latency network environments. With network round-trip time (RTT), the communication latency of secure aggregation is the product of protocol communication rounds and RTT. In a typical wide-area network environment with RTT of 100ms, traditional schemes have per-round aggregation latency of 300ms, while OPSA requires only 100ms, reducing latency overhead by 200ms. When training requires thousands of aggregation rounds, cumulative time savings can reach tens of minutes or hours.

From a theoretical communication complexity analysis, with n clients and m model parameters, SecAgg's single-round communication complexity is O(n² + n·m), while OPSA's communication complexity is O(n + n·m), eliminating the n² term and showing clear advantages in large-scale client scenarios. When the number of clients n reaches 1000, the dominance of the n² term in SecAgg's communication overhead makes the protocol nearly impractical, while OPSA's linear complexity scales well to large-scale scenarios.

### 5.2 Computational Overhead and TEE Memory Efficiency Comparison

In terms of TEE memory efficiency, OPSA's design demonstrates significant innovation. Existing TEE-based schemes (such as SEAR) attempt to alleviate memory bottlenecks by processing model parameters layer by layer within the TEE, but do not fundamentally reduce TEE's overall computational burden, still facing similar challenges when processing model layers with large numbers of parameters. SEAR adopts a layer-wise aggregation strategy, processing only one layer of model parameters within the TEE at a time. When a model contains layers with large numbers of parameters (e.g., fully connected layers with tens of millions of parameters), SEAR still faces TEE memory insufficiency.

OPSA offloads computation-intensive tasks (model aggregation and mask elimination) outside the TEE, handling only key operations within the TEE, decoupling TEE memory consumption from model scale. TEE only needs to store key information for each client (approximately 32 bytes/client) rather than the entire model. For large models with millions of parameters and hundreds of clients, TEE memory requirements drop from hundreds of MB to a few KB, completely solving the memory bottleneck. The reduction in memory footprint not only solves TEE's space limitations but also reduces the overhead of memory encryption/decryption operations, as the amount of data processed within the TEE is greatly reduced.

In terms of computational efficiency, experimental results show OPSA achieves 2 to 10 times speed improvement during multi-round aggregation. This performance improvement mainly comes from two sources: the reduction in communication rounds decreases the impact of network latency, particularly prominent in high-latency network environments; and TEE only handles lightweight key operations, avoiding the performance bottlenecks of processing large models within the TEE. Experimental data shows that in scenarios with 100 clients and millions of model parameters, KhPRF-OPSA's aggregation time is approximately one-fifth of SecAgg, and POT-OPSA's aggregation time is approximately one-third of SecAgg. POT-OPSA's aggregation time is slightly higher than KhPRF-OPSA due to the additional computational overhead introduced by its double-layer masking mechanism, but still shows significant performance improvement over traditional schemes.

### 5.3 Application Scenario Analysis

The OPSA protocol is suitable for various federated learning application scenarios, with clear advantages in the following contexts:

Cross-device federated learning scenarios. In federated learning scenarios involving large numbers of mobile devices or IoT devices, unstable network connections and frequent device dropout are common. OPSA's efficient dropout resilience mechanism and single-round communication mode make secure aggregation more practical in these scenarios. In Google's Gboard input method predictive model training, the number of participating mobile devices can reach millions, with device dropout rates exceeding 5%. Traditional SecAgg and similar schemes incur enormous communication overhead in such scenarios, while OPSA greatly improves system practicality through single-round communication aggregation and efficient TEE dropout handling.

High-latency network environments. In geographically distributed cross-regional federated learning scenarios (such as cross-national healthcare institution collaboration), network latency can become a performance bottleneck. OPSA reduces the communication rounds required for each aggregation from three to one, significantly reducing the impact of latency on training efficiency. In cross-Atlantic federated learning scenarios, network RTT can reach 150ms or more. OPSA saves 300ms of communication time per round, reducing cumulative training time by more than 66%.

Large model training scenarios. When training deep neural networks and other large models, OPSA avoids excessive consumption of TEE memory resources by offloading model aggregation operations from TEE internal to external servers, enabling secure aggregation of large models (such as ResNet-50, BERT, etc.). For modern deep learning models with tens of millions or even hundreds of millions of parameters, traditional TEE-based schemes cannot complete aggregation within 128MB of enclave memory, while OPSA is completely unconstrained by model scale.

Compliance scenarios requiring result auditing. In applications requiring auditing and traceability, such as financial regulation and medical data, OPSA's verification mechanism provides integrity guarantees for aggregation results, meeting compliance requirements. In federated learning scenarios for medical image analysis, according to HIPAA and other health data privacy regulations, the data processing process requires auditing. OPSA's commitment and signature mechanisms provide non-repudiable evidence for auditing, ensuring the integrity and traceability of the data processing process.

OPSA is also suitable for the following emerging applications: distributed model training in smart IoT, fleet learning for autonomous vehicles, collaborative learning for smart home devices, and more. With the rapid development of edge computing and IoT technology, federated learning application scenarios will continue to expand. OPSA, as an efficient and verifiable secure aggregation solution, has broad application prospects in these emerging scenarios.

## VI. Conclusion

This paper conducted a comprehensive research and analysis of OPSA—an efficient and verifiable one-pass secure aggregation protocol based on TEE. By delegating client dropout management to server-side TEE, OPSA designed two innovative masking protocols, KhPRF-OPSA and POT-OPSA, reducing communication rounds from three in traditional schemes to one. Through commitment and signature mechanisms, it achieved aggregation result verifiability, striking a good balance among communication efficiency, computational efficiency, and security.

OPSA's core innovations are reflected in three aspects: at the architectural level, by offloading model aggregation and mask elimination tasks outside the TEE, it fundamentally solves the computational bottleneck caused by TEE's limited memory, decoupling TEE memory consumption from model scale. At the protocol level, using novel cryptographic primitives such as KhPRF and POT, it achieves efficient and secure single-layer and double-layer mask aggregation, providing differentiated options for scenarios with different security requirements. At the verification level, a lightweight result verification mechanism is designed, achieving aggregation result verifiability with only O(1) additional communication overhead, filling the gap in result verification among existing secure aggregation protocols.

Reviewing from a course learning perspective, OPSA's protocol design fully reflects the integrated application of multiple core concepts from cryptography and network security courses: secure multi-party computation provides the theoretical foundation for secure aggregation, pseudo-random functions and key agreement protocols provide cryptographic tools for mask generation, commitment schemes and digital signature mechanisms provide security guarantees for result verification, and TEE trusted hardware provides the physical foundation for efficient protocol execution. This collaborative design philosophy of "cryptographic primitives + trusted hardware" represents an important development trend in modern security protocol design.

OPSA represents an important development direction for secure aggregation technology—dramatically improving performance while maintaining security through collaborative design of hardware-assisted security technology and cryptographic primitives. With the maturation and普及 of TEE technology (such as the widespread application of Intel SGX), TEE-based security solutions like OPSA are expected to play increasingly important roles in federated learning practice. However, OPSA's dependence on TEE hardware security is a potential security weakness, and future research needs to explore relaxation of hardware security assumptions.

Future research directions include: extending OPSA to Byzantine-robust secure aggregation scenarios, enabling the protocol to simultaneously resist privacy attacks and model poisoning attacks; exploring more efficient remote attestation mechanisms to reduce TEE certification overhead; combining OPSA with other privacy protection technologies (such as differential privacy) to build more comprehensive federated learning privacy protection frameworks; and deploying and evaluating OPSA's performance in real large-scale federated learning systems to provide empirical foundations for its practical application.

## References

[1] Kairouz P, McMahan H B, Avent B, et al. Advances and open problems in federated learning[J]. Foundations and Trends in Machine Learning, 2021, 14(1-2): 1-210.

[2] McMahan B, Moore E, Ramage D, et al. Communication-efficient learning of deep networks from decentralized data[C]//Artificial Intelligence and Statistics (AISTATS). PMLR, 2017: 1273-1282.

[3] Zhu L, Liu Z, Han S. Deep leakage from gradients[C]//Advances in Neural Information Processing Systems (NeurIPS), 2019: 14774-14784.

[4] Fredrikson M, Jha S, Ristenpart T. Model inversion attacks that exploit confidence information and basic countermeasures[C]//Proceedings of the 22nd ACM SIGSAC Conference on Computer and Communications Security (CCS). ACM, 2015: 1322-1333.

[5] Bonawitz K, Ivanov V, Kreuter B, et al. Practical secure aggregation for privacy-preserving machine learning[C]//Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security (CCS). ACM, 2017: 1175-1191.

[6] Bell J H, Bonawitz K A, Gascón A, et al. Secure aggregation with malicious clients[C]//29th USENIX Security Symposium. USENIX Association, 2020: 1277-1294.

[7] Guo Y, Polychroniadou A, Shi E, Byrd D, Balch T. MicroFedML: Privacy-preserving federated learning for small-weight scenarios[J]. Cryptology ePrint Archive, 2022.

[8] Ma Y, Woods J, Angel S, Polychroniadou A, Rabin T. Flamingo: Multi-round single-server secure aggregation with applications to private federated learning[C]//2023 IEEE Symposium on Security and Privacy (SP). IEEE, 2023: 977-995.

[9] Li H, Lin H, Polychroniadou A, Tessaro S. LERNA: Secure single-server aggregation via key-homomorphic masking[C]//Advances in Cryptology (CRYPTO). Springer, 2023: 289-318.

[10] Guan Z, Zhao Y, Wan Z, Han J. OPSA: Efficient and verifiable one-pass secure aggregation with TEE for federated learning[C]//IEEE Symposium on Security and Privacy (S&P). IEEE, 2025.

[11] Will N C, Maziero C A. Intel software guard extensions: A survey[J]. ACM Computing Surveys, 2023, 55(8): 1-37.

[12] Pass R, Shi E, Tramer F. Formal abstractions for attested execution secure processors[C]//Proceedings of the 36th Annual International Conference on the Theory and Applications of Cryptographic Techniques (EUROCRYPT). Springer, 2017: 260-289.

[13] Banerjee A, Peikert C, Rosen A. Pseudorandom functions and lattices[C]//Proceedings of the 31st Annual International Conference on the Theory and Applications of Cryptographic Techniques (EUROCRYPT). Springer, 2012: 719-737.

[14] Boneh D, Lewi K, Montgomery H, Raghunathan A. Key homomorphic PRFs and their applications[C]//Proceedings of the 33rd Annual International Cryptology Conference (CRYPTO). Springer, 2013: 410-428.

[15] Pedersen T P. Non-interactive and information-theoretic secure verifiable secret sharing[C]//Proceedings of the 11th Annual International Cryptology Conference (CRYPTO). Springer, 1991: 129-140.

[16] Choi S G, Katz J, Kumaresan R, Cid C. Multi-client non-interactive verifiable computation[C]//Theory of Cryptography Conference (TCC). Springer, 2013: 499-518.

[17] Zhao L, Jiang J, Feng B, et al. SEAR: Secure and efficient aggregation for Byzantine-robust federated learning[J]. IEEE Transactions on Dependable and Secure Computing, 2022, 19(5): 3329-3344.

[18] Van Schaik S, Seto A, Yurek T, et al. SoK: SGX.Fail: How often do TEEs fail?[C]//IEEE Symposium on Security and Privacy (S&P). IEEE, 2022.

[19] Jia Y, Liu S, Wang W, et al. HyperEnclave: An open and cross-platform trusted execution environment[C]//2022 USENIX Annual Technical Conference (USENIX ATC). USENIX Association, 2022: 437-454.

[20] Toffalini F, Payer M, Zhou J, Cavallaro L. Designing a provenance analysis for SGX enclaves[C]//Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses (RAID). 2023.
