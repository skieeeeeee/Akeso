"""The care-system branch: an allopathic visit stays short, an Ayurvedic one
runs the full examination.

Also guards the honest boundary: Homoeopathy, Unani and Siddha record the
patient's choice and share the diet/lifestyle enquiry, but do not get a
fabricated examination of their own.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.test_returning_patient import seed_returning, sign_in_demo

CORE_ANSWERS = {
    "e_complaint": "Stomach pain since yesterday",
    "e_onset": "Yesterday",
    "e_severity": "4",
    "e_describe": "Dull ache around the navel",
    "e_associated": "Vomiting",
    "e_tried": "Antacid",
    "e_meds_changed": "no",
    "e_new_conditions": "no",
    "e_anything_else": "no",
}


def walk(client, api, headers, encounter_id, *, answers=None, limit=60):
    """Answer everything the visit asks; return the ids asked, in order."""
    answers = {**CORE_ANSWERS, **(answers or {})}
    asked: list[str] = []
    view = client.get(f"{api}/encounters/{encounter_id}", headers=headers).json()
    for _ in range(limit):
        question = view.get("question")
        if not question:
            return asked, view
        asked.append(question["id"])
        # A single-choice question needs one of its own option values.
        text = answers.get(question["id"])
        if text is None:
            text = question["options"][0]["value"] if question["options"] else "no"
        view = client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={"instance_key": question["instance_key"], "text": text, "input_method": "touch"},
            headers=headers,
        ).json()
    raise AssertionError("visit did not terminate")


def start(client, api, headers, system: str):
    started = client.post(f"{api}/encounters/start", json={}, headers=headers).json()
    assert started["question"]["id"] == "e_care_system"
    view = client.post(
        f"{api}/encounters/{started['encounter_id']}/answer",
        json={"instance_key": "e_care_system", "text": system, "input_method": "touch"},
        headers=headers,
    ).json()
    return started["encounter_id"], view


class TestTheQuestionItself:
    def test_a_visit_opens_by_asking_which_system(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        view = client.post(f"{api}/encounters/start", json={}, headers=headers).json()

        question = view["question"]
        assert question["id"] == "e_care_system"
        assert question["required"] is True
        assert question["allow_none"] is False
        values = {option["value"] for option in question["options"]}
        assert values == {
            "allopathy", "ayurveda", "homoeopathy", "unani",
            "siddha", "yoga_naturopathy", "unsure",
        }

    def test_the_choice_is_recorded_on_the_visit(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "ayurveda")
        view = client.get(f"{api}/encounters/{encounter_id}", headers=headers).json()
        assert view["care_system"] == "ayurveda"

    def test_the_choice_is_remembered_for_next_time(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        start(client, api, headers, "ayurveda")
        patient = client.get(f"{api}/patients/me", headers=headers).json()
        # Pre-selected next visit, so a returning patient is not asked cold.
        assert patient["preferred_care_system"] == "ayurveda"

    def test_a_nonsense_system_does_not_open_ayush(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        started = client.post(f"{api}/encounters/start", json={}, headers=headers).json()
        view = client.post(
            f"{api}/encounters/{started['encounter_id']}/answer",
            json={"instance_key": "e_care_system", "text": "astrology", "input_method": "text"},
            headers=headers,
        ).json()
        # Recorded as nothing, and no examination sections opened.
        assert view["progress"]["section_count"] == 4


class TestAllopathyStaysShort:
    def test_it_asks_only_about_today(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "allopathy")
        asked, final = walk(client, api, headers, encounter_id)

        assert final["complete"] is True
        # No AYUSH question appears.
        assert not [question for question in asked if question.startswith("ay_")]
        # The whole visit is around ten questions.
        assert len(asked) <= 12

    def test_no_ayush_assessment_is_created(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "allopathy")
        walk(client, api, headers, encounter_id)
        assert client.get(f"{api}/ayush", headers=headers).json() is None


class TestAyurvedaRunsTheFullExamination:
    def test_it_adds_the_ayush_sections(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        _, view = start(client, api, headers, "ayurveda")
        # system + today + detail + changes + three AYUSH sections
        assert view["progress"]["section_count"] == 7

    def test_it_asks_substantially_more_than_allopathy(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db, "standard")
        seed_returning(db, "easy")

        allopathic = sign_in_demo(client, api, "standard")
        allo_id, _ = start(client, api, allopathic, "allopathy")
        allo_asked, _ = walk(client, api, allopathic, allo_id)

        ayurvedic = sign_in_demo(client, api, "easy")
        ayur_id, _ = start(client, api, ayurvedic, "ayurveda")
        ayur_asked, ayur_final = walk(client, api, ayurvedic, ayur_id)

        assert ayur_final["complete"] is True
        # The stated requirement: 30+ for AYUSH, and the allopathic visit
        # stays as short as it was.
        assert len(ayur_asked) >= 30
        assert len(ayur_asked) > len(allo_asked) * 2

    def test_it_covers_dashavidha_ashtasthana_and_lifestyle(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "ayurveda")
        asked, _ = walk(client, api, headers, encounter_id)

        assert len([q for q in asked if q.startswith("ay_dash_")]) == 10
        assert len([q for q in asked if q.startswith("ay_ashta_")]) == 8
        assert len([q for q in asked if q.startswith("ay_life_")]) == 4
        assert "ay_ahara" in asked
        assert "ay_vihara" in asked

    def test_answers_land_in_the_ayush_assessment(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "ayurveda")
        walk(client, api, headers, encounter_id)

        assessment = client.get(f"{api}/ayush", headers=headers).json()
        assert assessment is not None
        assert len(assessment["dashavidha"]) == 10
        assert len(assessment["ashtasthana"]) == 8
        assert len(assessment["lifestyle"]) == 4
        assert assessment["ahara"]
        assert assessment["is_complete"] is True
        assert assessment["answered_count"] >= 24

    def test_ayush_answers_never_reach_the_medical_profile(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        before = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
        encounter_id, _ = start(client, api, headers, "ayurveda")
        walk(client, api, headers, encounter_id)
        after = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()

        # Constitution is not an allopathic clinical fact; it belongs to the
        # AYUSH assessment only.
        assert after["sections"] == before["sections"]

    def test_the_review_reports_ayush_was_included(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "ayurveda")
        walk(client, api, headers, encounter_id)
        history = client.get(
            f"{api}/patients/me/medical-profile/structured", headers=headers
        ).json()
        assert history["ayush_included"] is True


class TestPartialAyushSystemsAreHonest:
    def test_they_share_only_the_lifestyle_enquiry(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        _, view = start(client, api, headers, "homoeopathy")
        # system + today + detail + changes + lifestyle only.
        assert view["progress"]["section_count"] == 5

    def test_they_do_not_get_a_fabricated_examination(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "unani")
        asked, _ = walk(client, api, headers, encounter_id)

        # No Dashavidha or Ashtasthana: those are Ayurvedic frameworks and
        # inventing a Unani equivalent would be dishonest.
        assert not [q for q in asked if q.startswith("ay_dash_")]
        assert not [q for q in asked if q.startswith("ay_ashta_")]
        # The genuinely shared diet/lifestyle questions are asked.
        assert [q for q in asked if q.startswith("ay_life_")]

    def test_the_choice_is_still_recorded(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = start(client, api, headers, "siddha")
        view = client.get(f"{api}/encounters/{encounter_id}", headers=headers).json()
        assert view["care_system"] == "siddha"


class TestAyushContentEndpoint:
    def test_it_serves_the_full_examination(self, client: TestClient, api: str):
        body = client.get(f"{api}/ayush/content").json()
        assert len(body["dashavidha"]) == 10
        assert len(body["ashtasthana"]) == 8
        assert len(body["lifestyle"]) == 4
        assert body["total_factors"] == 24

        keys = {item["key"] for item in body["ashtasthana"]}
        assert keys == {
            "nadi", "mutra", "mala", "jihva",
            "shabda", "sparsha", "drik", "akriti",
        }
        for item in [*body["dashavidha"], *body["ashtasthana"], *body["lifestyle"]]:
            # Each carries its Sanskrit term alongside a plain-language prompt.
            assert item["term"]
            assert set(item["prompt"]) >= {"en", "hi"}

    def test_a_tampered_answer_is_rejected(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        response = client.put(
            f"{api}/ayush",
            json={"ashtasthana": {"nadi": "levitating"}},
            headers=headers,
        )
        assert response.status_code == 422

    def test_an_invented_factor_is_rejected(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        response = client.put(
            f"{api}/ayush", json={"lifestyle": {"horoscope": "leo"}}, headers=headers
        )
        assert response.status_code == 422
        assert "horoscope" in response.json()["error"]["message"]

    def test_the_manas_question_offers_a_decline(self, client: TestClient, api: str):
        body = client.get(f"{api}/ayush/content").json()
        manas = next(item for item in body["lifestyle"] if item["key"] == "manas")
        # Mental state is sensitive; declining must be a first-class option.
        assert "prefer_not" in {option["value"] for option in manas["options"]}


class TestAHindiVisitIsRecordedInHindi:
    """A choice answer must read back in the language it was given in.

    The client posts the option's machine value, so without this the review
    screen shows a Hindi patient the English option value they never saw.
    """

    def test_choice_answers_read_back_in_hindi(self, client: TestClient, api: str, db):
        # Kamla Devi is the Hindi-speaking demo patient.
        seed_returning(db, "easy")
        headers = sign_in_demo(client, api, "easy")
        encounter_id, _ = start(client, api, headers, "ayurveda")
        walk(client, api, headers, encounter_id, answers={
            "e_complaint": "घुटनों में दर्द",
            "e_onset": "कल से",
            "e_describe": "सुबह ज़्यादा",
            "e_associated": "कुछ नहीं",
            "e_tried": "कुछ नहीं",
        })

        review = client.get(f"{api}/encounters/{encounter_id}/review", headers=headers).json()
        answers = [row["answer"] for row in review["today_answers"]]
        assert answers, "the review screen listed nothing"
        # Every answer either is Devanagari or is a number the patient typed.
        latin = [a for a in answers if any("a" <= c.lower() <= "z" for c in a)]
        assert latin == [], latin

    def test_the_machine_value_still_drives_the_branch(
        self, client: TestClient, api: str, db
    ):
        """Localising the record must not localise the logic."""
        seed_returning(db, "easy")
        headers = sign_in_demo(client, api, "easy")
        encounter_id, _ = start(client, api, headers, "ayurveda")
        walk(client, api, headers, encounter_id)

        # The AYUSH sections opened...
        assessment = client.get(f"{api}/ayush", headers=headers).json()
        assert len(assessment["dashavidha"]) == 10
        # ...and the assessment holds controlled vocabulary, not Hindi labels.
        assert assessment["dashavidha"]["prakriti"] in ("vata", "pitta", "kapha", "mixed", "unsure")
        # And the encounter remembers the system as an enum.
        encounter = client.get(f"{api}/encounters/{encounter_id}", headers=headers).json()
        assert encounter["care_system"] == "ayurveda"
