# Lessons Learned

## Structured Output Matters

Free-form itinerary text is easy to read but hard to validate. The project needs machine-checkable output because later steps inspect dates, weather, activities, prices, and traveler feedback.

Structured JSON makes the itinerary usable by Python code. It allows the notebook to parse the result, validate it with Pydantic, calculate costs, run evals, and pass a stable object into the revision loop.

Without structured output, every downstream step becomes string parsing.

## Schemas Should Be Included In Prompts

The model needs to know the exact target shape before it generates the answer. Including the Pydantic-derived schema in the prompt reduces ambiguity around required fields, nested objects, dates, and lists.

This is especially important for nested output like:

- Travel plan.
- Itinerary days.
- Weather objects.
- Activity objects.
- Activity recommendation reasons.

If the schema is not included, the model may produce a plausible itinerary that is not parseable by the code.

## Evals Need To Be Explicit

The itinerary can look good while still failing requirements. Useful evals need to check specific claims:

- Do dates match?
- Are activities real?
- Is total cost correct?
- Is cost within budget?
- Do activities match traveler interests?
- Are activities appropriate for the weather?
- Was traveler feedback incorporated?

Vague evaluation like "is this a good itinerary" is too weak. The project works better when each eval has a concrete failure reason.

## The ReAct Loop Needs Strict Formatting

The revision agent is only useful if Python can parse its action. The model must return:

```text
THOUGHT:
...
ACTION:
{"tool_name": "...", "arguments": {...}}
```

If the model adds prose, omits `ACTION`, or emits malformed JSON, the loop cannot safely execute tools.

Strict formatting also improves debugging. The trace shows what the agent intended to do, which tool ran, and what observation came back.

## Weather/Activity Compatibility Is Hard For Simple Rules

Some weather decisions are not simple keyword matches. An outdoor event might be acceptable in clear weather, unacceptable in a thunderstorm, or acceptable during rain only if the description says it can move indoors.

Simple rules can catch obvious cases but miss conditional language. LLM-assisted evaluation can help compare activity descriptions against weather, but it still needs clear criteria and should not be treated as perfect.

## Pydantic Helps Catch Invalid LLM Output

Pydantic catches structural problems:

- Missing required fields.
- Wrong data types.
- Invalid dates.
- Incorrect nested object shapes.
- Malformed JSON that cannot become a model.

Pydantic does not prove that the itinerary is good. It proves that the object has the expected structure. Content quality still needs eval functions.

## The Planner And Revision Agent Have Different Jobs

The Expert Planner should generate a strong first itinerary from complete context. The Resourceful Itinerary Revision Agent should inspect that plan, call tools, run evals, and revise based on failures or feedback.

Keeping these stages separate makes it easier to diagnose whether a problem came from initial generation, validation, eval criteria, or tool-loop behavior.

## Output Evidence Should Stay Honest

Outputs should be saved from real notebook runs. They should not be manually rewritten to look cleaner or more successful.

If an eval fails, keep the failure when it is useful for debugging. If a fix is applied, save the new run evidence separately or clearly replace it with the actual new output.
