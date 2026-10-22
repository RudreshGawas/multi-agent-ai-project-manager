from pydantic import BaseModel, Field, ValidationInfo, field_validator


class ClarifyingQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    options: list[str] = Field(min_length=2, max_length=5)
    suggested_answer: str = Field(min_length=1, max_length=200)

    @field_validator("suggested_answer")
    @classmethod
    def suggested_answer_must_be_an_option(
        cls,
        value: str,
        info: ValidationInfo,
    ) -> str:
        if value not in info.data.get("options", []):
            raise ValueError("Suggested answer must match one of the options.")
        return value


class ClarificationResponse(BaseModel):
    questions: list[ClarifyingQuestion] = Field(max_length=3)


class ClarificationAnswer(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    answer: str = Field(min_length=1, max_length=500)
