[![Gemini API](https://ai.google.dev/_static/googledevai/images/lockup-new.svg)](/)

`/`

- [English](https://ai.google.dev/gemini-api/docs/openai)
- [Deutsch](https://ai.google.dev/gemini-api/docs/openai?hl=de)
- [Español – América Latina](https://ai.google.dev/gemini-api/docs/openai?hl=es-419)
- [Français](https://ai.google.dev/gemini-api/docs/openai?hl=fr)
- [Indonesia](https://ai.google.dev/gemini-api/docs/openai?hl=id)
- [Italiano](https://ai.google.dev/gemini-api/docs/openai?hl=it)
- [Polski](https://ai.google.dev/gemini-api/docs/openai?hl=pl)
- [Português – Brasil](https://ai.google.dev/gemini-api/docs/openai?hl=pt-br)
- [Tiếng Việt](https://ai.google.dev/gemini-api/docs/openai?hl=vi)
- [Türkçe](https://ai.google.dev/gemini-api/docs/openai?hl=tr)
- [עברית](https://ai.google.dev/gemini-api/docs/openai?hl=he)
- [العربيّة](https://ai.google.dev/gemini-api/docs/openai?hl=ar)
- [हिंदी](https://ai.google.dev/gemini-api/docs/openai?hl=hi)
- [ภาษาไทย](https://ai.google.dev/gemini-api/docs/openai?hl=th)
- [中文 – 简体](https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn)
- [中文 – 繁體](https://ai.google.dev/gemini-api/docs/openai?hl=zh-tw)
- [日本語](https://ai.google.dev/gemini-api/docs/openai?hl=ja)
- [한국어](https://ai.google.dev/gemini-api/docs/openai?hl=ko)

[Sign in](https://ai.google.dev/_d/signin?continue=https%3A%2F%2Fai.google.dev%2Fgemini-api%2Fdocs%2Fopenai&prompt=select_account)

- On this page
- [Streaming](#streaming)
- [Function calling](#function-calling)
- [Embeddings](#embeddings)
- [Current limitations](#current-limitations)

Grounding with Google Search is now available! [Learn more](https://developers.googleblog.com/en/gemini-api-and-ai-studio-now-offer-grounding-with-google-search)

- [Home](https://ai.google.dev/)
- [Gemini API](https://ai.google.dev/gemini-api)
- [Docs](https://ai.google.dev/gemini-api/docs)

Was this helpful?



 Send feedback



# OpenAI compatibility

bookmark\_borderbookmark

 Stay organized with collections


 Save and categorize content based on your preferences.


- On this page
- [Streaming](#streaming)
- [Function calling](#function-calling)
- [Embeddings](#embeddings)
- [Current limitations](#current-limitations)

Gemini models are accessible using the OpenAI libraries (Python and TypeScript /
Javascript) along with the REST API, by updating three lines of code
and using your [Gemini API key](https://aistudio.google.com/apikey). If you
aren't already using the OpenAI libraries, we recommend that you call the
[Gemini API directly](https://ai.google.dev/gemini-api/docs/quickstart).

[Python](#python)[Node.js](#node.js)[REST](#rest)More

```
from openai import OpenAI

client = OpenAI(
    api_key="gemini_api_key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-1.5-flash",
    n=1,
    messages=[\
        {"role": "system", "content": "You are a helpful assistant."},\
        {\
            "role": "user",\
            "content": "Explain to me how AI works"\
        }\
    ]
)

print(response.choices[0].message)

```

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: "gemini_api_key",
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
});

const response = await openai.chat.completions.create({
    model: "gemini-1.5-flash",
    messages: [\
        { role: "system", content: "You are a helpful assistant." },\
        {\
            role: "user",\
            content: "Explain to me how AI works",\
        },\
    ],
});

console.log(response.choices[0].message);

```

```
curl "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer gemini_api_key" \
-d '{
    "model": "gemini-1.5-flash",
    "messages": [\
        {"role": "user", "content": "Explain to me how AI works"}\
    ]
    }'

```

## Streaming

The Gemini API supports [streaming responses](/gemini-api/docs/text-generation?lang=python#generate-a-text-stream).

[Python](#python)[Node.js](#node.js)[REST](#rest)More

```
from openai import OpenAI

client = OpenAI(
    api_key="gemini_api_key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
  model="gemini-1.5-flash",
  messages=[\
    {"role": "system", "content": "You are a helpful assistant."},\
    {"role": "user", "content": "Hello!"}\
  ],
  stream=True
)

for chunk in response:
    print(chunk.choices[0].delta)

```

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: "gemini_api_key",
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: "gemini-1.5-flash",
    messages: [\
      {"role": "system", "content": "You are a helpful assistant."},\
      {"role": "user", "content": "Hello!"}\
    ],
    stream: true,
  });

  for await (const chunk of completion) {
    console.log(chunk.choices[0].delta.content);
  }
}

main();

```

```
curl "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer gemini_api_key" \
-d '{
    "model": "gemini-1.5-flash",
    "messages": [\
        {"role": "user", "content": "Explain to me how AI works"}\
    ],
    "stream": true
  }'

```

## Function calling

Function calling makes it easier for you to get structured data outputs from
generative models and is [supported in the Gemini API](/gemini-api/docs/function-calling/tutorial?lang=python).

[Python](#python)[Node.js](#node.js)[REST](#rest)More

```
from openai import OpenAI

client = OpenAI(
    api_key="gemini_api_key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

tools = [\
  {\
    "type": "function",\
    "function": {\
      "name": "get_weather",\
      "description": "Get the weather in a given location",\
      "parameters": {\
        "type": "object",\
        "properties": {\
          "location": {\
            "type": "string",\
            "description": "The city and state, e.g. Chicago, IL",\
          },\
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},\
        },\
        "required": ["location"],\
      },\
    }\
  }\
]

messages = [{"role": "user", "content": "What's the weather like in Chicago today?"}]
response = client.chat.completions.create(
  model="gemini-1.5-flash",
  messages=messages,
  tools=tools,
  tool_choice="auto"
)

print(response)

```

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: "gemini_api_key",
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
});

async function main() {
  const messages = [{"role": "user", "content": "What's the weather like in Chicago today?"}];
  const tools = [\
      {\
        "type": "function",\
        "function": {\
          "name": "get_weather",\
          "description": "Get the weather in a given location",\
          "parameters": {\
            "type": "object",\
            "properties": {\
              "location": {\
                "type": "string",\
                "description": "The city and state, e.g. Chicago, IL",\
              },\
              "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},\
            },\
            "required": ["location"],\
          },\
        }\
      }\
  ];

  const response = await openai.chat.completions.create({
    model: "gemini-1.5-flash",
    messages: messages,
    tools: tools,
    tool_choice: "auto",
  });

  console.log(response);
}

main();

```

```
curl "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer gemini_api_key" \
-d '{
  "model": "gemini-1.5-flash",
  "messages": [\
    {\
      "role": "user",\
      "content": "What'\''s the weather like in Chicago today?"\
    }\
  ],
  "tools": [\
    {\
      "type": "function",\
      "function": {\
        "name": "get_weather",\
        "description": "Get the current weather in a given location",\
        "parameters": {\
          "type": "object",\
          "properties": {\
            "location": {\
              "type": "string",\
              "description": "The city and state, e.g. Chicago, IL"\
            },\
            "unit": {\
              "type": "string",\
              "enum": ["celsius", "fahrenheit"]\
            }\
          },\
          "required": ["location"]\
        }\
      }\
    }\
  ],
  "tool_choice": "auto"
}'

```

## Embeddings

Text embeddings measure the relatedness of text strings and can be generated
using the [the Gemini API](/gemini-api/docs/embeddings).

[Python](#python)[Node.js](#node.js)[REST](#rest)More

```
from openai import OpenAI

client = OpenAI(
    api_key="gemini_api_key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-004"
)

print(response.data[0].embedding)

```

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: "gemini_api_key",
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
});

async function main() {
  const embedding = await openai.embeddings.create({
    model: "text-embedding-004",
    input: "Your text string goes here",
  });

  console.log(embedding);
}

main();

```

```
curl "https://generativelanguage.googleapis.com/v1beta/openai/embeddings" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer gemini_api_key" \
-d '{
    "input": "Your text string goes here",
    "model": "text-embedding-004"
  }'

```

## Current limitations

Support for the OpenAI libraries is still in beta while we extend feature support.
The following functionalities are limited:

- [Image upload](/gemini-api/docs/vision?lang=python) using a URL / Base64
- [Structured output](/gemini-api/docs/structured-output?lang=python)

If you have questions about supported parameters, upcoming features, or run into
any issues getting started with Gemini, join our [Developer Forum](https://discuss.ai.google.dev/c/gemini-api/4).

Was this helpful?



 Send feedback



Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-11-12 UTC.


Need to tell us more?


\[\[\["Easy to understand","easyToUnderstand","thumb-up"\],\["Solved my problem","solvedMyProblem","thumb-up"\],\["Other","otherUp","thumb-up"\]\],\[\["Missing the information I need","missingTheInformationINeed","thumb-down"\],\["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"\],\["Out of date","outOfDate","thumb-down"\],\["Samples / code issue","samplesCodeIssue","thumb-down"\],\["Other","otherDown","thumb-down"\]\],\["Last updated 2024-11-12 UTC."\],\[\],\[\]\]
