# Algorithms and Data Structures – Semestral Projects

This repository contains two semestral projects developed for the university course **Algorithms and Data Structures**.

The main objective of both projects was to design and implement complex data structures from scratch and apply them in practical information systems.

All implementations were written in **Python**.

---

# 📌 Project 1 – K-D Tree (Multidimensional Search Structure)

### Overview

Implementation of a generalized **K-D Tree** supporting multi-dimensional keys and duplicate values.

The data structure was applied in a demonstrational information system for managing:

- Real estate properties
- Land parcels
- GPS-based spatial data

### Key Features

- Custom K-D Tree implementation (no built-in libraries)
- Support for:
  - Insert
  - Search
  - Delete
  - Update
- Duplicate key handling
- Non-recursive traversal logic
- Complexity analysis of operations
- CSV export/import support
- GUI layer interacting with the system

The system was designed with emphasis on:
- Efficient spatial querying
- Memory optimization
- Correct structural maintenance after deletion operations

---

# 📌 Project 2 – HeapFile & Extendible Hashing (File-Based Storage)

### Overview

Implementation of file-based data structures simulating persistent storage on disk:

- **HeapFile** (unsorted file structure)
- **Extendible Hashing (HashFile)**

The structures were applied in an information system for managing auto service visit records.

### Key Features

- Custom binary block storage
- Block chaining for partially and fully free blocks
- Persistent storage (application restart-safe)
- Extendible hashing with:
  - Directory doubling
  - Block splitting
  - Dynamic depth handling
- Optimized number of disk accesses per operation
- Analysis of read/write operation counts

The system allows:
- Insert
- Search
- Update
- Delete
- Record persistence across sessions

---

# 🧠 Implemented Concepts

- Advanced tree structures (K-D Tree)
- Extendible hashing
- File-based data storage simulation
- Block-level disk access optimization
- Object-Oriented Design
- Interface-like abstractions in Python
- Complexity and I/O access analysis

---

# ⚠️ Note

The current codebase is written in Slovak (variable and class names).  
A refactored English version will be added in the future for international readability.
