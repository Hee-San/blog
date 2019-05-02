---
title: "{{ replace .Name "_" " " | title }}"
date: {{ .Date }}
archives: ["{{ dateFormat "2006/01" .Date }}"]
tags: []
---
