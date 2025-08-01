# 📰 MyNews – Automated Daily Blog Generator with Hugo & Mistral

**MyNews** is a fully automated blog system that generates and publishes a new English article every day using the [Mistral AI API](https://docs.mistral.ai/), built with [Hugo](https://gohugo.io/) and deployed via GitHub Actions to GitHub Pages.

## 🚀 Features

- 🧠 AI-generated titles & articles (via Mistral)
- 🛠️ Built with Hugo static site generator (theme: Ananke)
- 📅 Automatically posts a new article daily (8am UTC)
- ☁️ Deployed to GitHub Pages using CI/CD
- 💸 Monetization-ready: Amazon Affiliate links and Google AdSense support

## 🧰 Technologies Used

- Python (`generate_article.py`)
- Hugo (static site generator)
- GitHub Actions (CI/CD workflows)
- Mistral API (AI content generation)
- YAML, Markdown

## 🔄 Workflows

| Name | Description | Trigger |
|------|-------------|---------|
| `daily_article.yml` | Generates and commits a new article every day | Daily at 08:00 UTC |
| `deploy.yml`        | Builds the Hugo site and deploys it to GitHub Pages | On push to `main` |

## 📄 Example Article Format

```yaml
---
title: "Why Global Markets Reacted to Fed’s Interest Rate Decision"
date: 2025-08-01
draft: false
---
Introduction...

Main paragraphs...

Conclusion...

---

📦 Check out related products on Amazon: [Buy Now](https://www.amazon.com/s?k=why-global-markets-reacted&tag=your-affiliate-tag)




