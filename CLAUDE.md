# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This project aims to create a datawarehouse for Jortt, a book-keeping app. It ingests data using dlt with the Jortt API https://developer.jortt.nl/#jortt-api as the source and DuckDB as the destination. The database is used using marimo as a front end.

 
Jortt API → dlt pipeline → DuckDB → marimo 

## Development conventions

- Use dlt pipeline as much as possible with the least amount of vanilla Python
