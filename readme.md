## Wiki scraper

#### Description

A simple tool to collect some English text data from Wikipedia.

It looks for the main content div ``@id='mw-content-text'`` in Wiki page, collects text data, and walks through links in a tree way.

Use Python + Selenium for a multi-threaded web spider. And Rust for the processing of collected data ( Rust is fast and really easy to write when dealing with text data due to the wonderful syntax ).

#### Dependency

```text
python >= "3.9"
python.selenium >= "4.1.2"
python.webdriver-manager >= "3.5.3"
rust >= "1.8"
```

#### Use

To run spider :

```bash
py scraper.py
# or
py scraper-parallel.py
```

To run text_processor :

```bash
cd text_processor
cargo run --release
```

#### Goal

Do some English NLP things. Maybe in Rust. But data from Wikipedia seems have some bias when doing NLP. Words that is meaningful only with a viewpoint is hardly happened, like **"hurry"**.

*Last update: 2022/03/11*

---

#### Update

* 2022/03/10
  * Start with a simple web spider in Python
  * Try to do a parallelized web spider
* 2022/03/11
  * Finish an easy multiple worker spider, it can collect at the speed of about 40 kb per second with 4G network
  * Finish an easy text processor that collects the times appearing for every 5-length word.

