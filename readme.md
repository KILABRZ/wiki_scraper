## Wiki scraper

#### Description

A simple tool to collect some English text data from Wikipedia.

It looks for the main content div ``@id='mw-content-text'`` in Wiki page, collects text data, and walks through links in a tree way.

Use Python + Selenium for web spider. And Rust for processing of collected data ( Rust is fast and really easy to write when dealing with text data due to the wonderful syntax ).

#### Dependency

```text
python >= "3.9"
python.selenium >= "4.1.2"
python.webdriver-manager >= "3.5.3"
rust >= "1.8"
```

#### Goal

Do some English NLP things. Maybe in Rust.

*Last update: 2022/03/10*

---

#### Update

* 2022/03/10
  * Start with a simple web spider in Python

