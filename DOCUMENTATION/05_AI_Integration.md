# 05 – AI Integration

## 1. Purpose
The AI assistant provides preliminary decision support by analysing grievance text. It can suggest:
- Concerned department
- Grievance category
- Priority (Low, Medium or High)
- Concise summary
- Possible duplicate candidates, if duplicate detection is implemented and enabled

## 2. Processing flow
1. An authorized CMO user requests analysis for a grievance.
2. The backend retrieves the grievance text.
3. The AI integration prepares a constrained analysis request.
4. The external model is called when configured and available.
5. The backend parses and validates the result against supported department/category/priority values.
6. Suggestions are stored separately from official grievance fields.
7. The CMO reviews and approves or rejects the suggestions.
8. Only an authorized human review should apply suggestions to official grievance fields.

## 3. External model configuration
Configure the API key only in `backend/.env`, never in frontend code:
```env
GEMINI_API_KEY=replace_with_your_own_key
GEMINI_MODEL=gemini-3.8-flash
```
The model identifier should be checked against the current provider documentation and account availability. Do not commit the actual key.

## 4. Fallback behaviour
The project has returned `analysis_provider: local_fallback` when the external model service was unavailable. This is a keyword-based fallback and is not equivalent to a generative model. Responses should clearly identify fallback use and state that the result is preliminary.

## 5. Human-in-the-loop and safeguards
- AI suggestions are not official decisions.
- CMO review is required before applying suggestions.
- Invalid model output must be rejected or mapped safely; never trust arbitrary model-generated IDs or SQL.
- Do not send unnecessary personal information to the external model.
- Handle API errors, rate limits, unavailable models and malformed responses.
- Log provider/fallback metadata without logging secrets or excessive personal data.
- Do not claim duplicate detection is operational unless the relevant implementation is enabled and tested.

## 6. Evaluation
A production-quality system should evaluate department/category accuracy, priority agreement, summary quality, fallback frequency, latency and failure rate on a reviewed, representative dataset. The current recruitment prototype should not claim validated real-world accuracy without measured evidence.
