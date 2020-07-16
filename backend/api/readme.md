# Question API
Api for quiz questions. Route and example request:
`GET /questions?num=1`. Default number of returned questions is 3.

Example response:
```
[
    {
        "question": "Najbardziej prymitywnym systemem liczbowym jest:",
        "answers": [
            {
                "answer": "dwójkowy system liczbowy",
                "is_correct": false
            },
            {
                "answer": "jedynkowy system liczbowy",
                "is_correct": true
            },
            {
                "answer": "szesnastkowy system liczbowy",
                "is_correct": false
            }
        ]
    }
]
```

Questions come from the src/api/data/questions.json file. No difficulty levels, categorized, varying number of possible and correct answers (at least one).
