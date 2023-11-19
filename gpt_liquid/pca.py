from pydantic import BaseModel, Field


class ProstateCancer(BaseModel):
    ipsa: str
    t_stage: str | None = Field(default=None)
    n_stage: str | None = Field(default=None)
    m_stage: str | None = Field(default=None)
    gleason: str | None = Field(default=None)
    diagnose: str
    therapy: str

    model_config = {"extra": "ignore"}


PCA_EXAMPLES: list[tuple[ProstateCancer, str]] = [
    (
        ProstateCancer(
            ipsa="5.2",
            t_stage="T1",
            n_stage="N0",
            m_stage="M0",
            gleason="3+3",
            diagnose="prostaatkanker",
            therapy="radicale prostatectomie",
        ),
        """
    Beste collega,

    Na vastellen van een verhoogde PSA waarde van 5.2 ng/ml, hebben we een prostaatbiopsie uitgevoerd.
    De resultaten van de prostaatbiopsie zijn als volgt:
    De diagnose is prostaatkanker, stadium T1N0M0, met een Gleason score van 3+3.
    We adviseren een radicale prostatectomie.

    Met vriendelijke groet,
    """,
    ),
    (
        ProstateCancer(
            ipsa="1.2",
            diagnose="Geen prostaatkanker",
            therapy="watchful waiting",
        ),
        """
    Beste collega,

    Na vaststellen van een verhoogde PSA waarde van 1.2 ng/ml, hebben we een prostaatbiopsie uitgevoerd.
    De diagnose is geen prostaatkanker.
    We adviseren een watchful waiting beleid.

    Met vriendelijke groet,
    """,
    ),
]
