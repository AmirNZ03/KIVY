name: Build APK

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y \
            python3-pip \
            git \
            zip \
            unzip \
            openjdk-17-jdk
          pip install --upgrade pip
          pip install buildozer cython

      - name: Build APK
        run: |
          buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: MyApp-APK
          path: bin/*.apk
