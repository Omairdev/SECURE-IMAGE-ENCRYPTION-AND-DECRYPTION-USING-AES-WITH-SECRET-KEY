# SECURE-IMAGE-ENCRYPTION-AND-DECRYPTION-USING-AES-WITH-SECRET-KEY
# 🔐 Secure Image Encryption & Decryption using AES

<p align="center">
  <b>Protecting Digital Images with Strong Cryptography & Seamless UX</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask">
  <img src="https://img.shields.io/badge/Security-AES%20CBC-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>



## 🚀 Overview

A secure web application that encrypts and decrypts images using **AES (Advanced Encryption Standard) in CBC mode**.  
Designed to protect sensitive visual data with a **secret key-based system**, ensuring confidentiality and secure access.



## ✨ Key Features

- 🔐 **AES Encryption (CBC Mode)** for strong security  
- 🧑‍💻 **User Authentication** (Login & Registration)  
- 🖼️ **Image Upload & Management**  
- 🔑 **Secret Key-Based Decryption**  
- ⚡ **Fast & Efficient Processing**  
- 🎯 **Clean, User-Friendly Interface**  



## 🧠 How It Works

```mermaid
flowchart LR
A[User Login] --> B[Upload Image]
B --> C[Encrypt using AES]
C --> D[Encrypted Image Stored]
D --> E[Enter Secret Key]
E --> F[Decrypt Image]
