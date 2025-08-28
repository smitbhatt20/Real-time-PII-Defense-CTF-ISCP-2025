# Real-time-PII-Defense-CTF-ISCP-2025
Python solution for detecting and redacting Personally Identifiable Information (PII) in CSV datasets, developed for the ISCP 2025 CTF challenge.

This repository contains a Python solution for detecting and redacting Personally Identifiable Information (PII) from CSV datasets. The project was developed as part of the ISCP 2025 CTF challenge.

The main goal is to prevent PII leaks and demonstrate a working PII detection system.

Features:

1.Detects standalone PII:
2.Phone numbers (10-digit)
3.Aadhar numbers (12-digit)
4.Passport numbers
5.UPI IDs

Detects combinatorial PII:
Full names + emails
Addresses tied to individuals
Device IDs/IPs linked to users

Automatically redacts identified PII ([REDACTED])

Adds a column is_pii indicating whether the row contains PII

Searches for ISCP flag in the dataset
