import pytest

from .string_distance_measurer import StringDistanceMeasurer


ALLOWED_TOLERANCE = 0.01


class TestStringDistanceMeasurer:

    @pytest.mark.parametrize(
        "sent1, sent2, expected_distance",
        [
            (
                    "Tomarow come check us out if your in the area show starts at 6:00pm 2404 E. La Palma Anaheim, California 92806 Cost:$3",
                    "Tomorrow you can check us if you area will show start at 6 pm 2404 East La Palma Anaheim, $3",
                    0.622
            ),
            # original posting and its yahoo.com search snapshot
            (
                    "Fliers may have to wait years for new liquid screening equipment",
                    "for screening checkpoints and equipment; improving ... Wait times are not just a problem at large airports",
                    0.383
            ),
            # slang and search snippet
            (
                    "hell yea i stay in california. and hell no lol LA sucks hella bad, i lived there for a while and hated it sooo much, so boring! ",
                    "My life is so boring without Tree Hill and the OC. America is sooo racist I LOVE YOU SO MUCH. TO everyone that has hurt me...no one in the ..... Yeah sucks I know",
                    0.417
            ),
            (
                    "I think its gonna be in the east coast as well. California is pretty but way to close to LA and helicopters are gonna ruin it",
                    "could be in east coast as well. California is pretty but way to close to LA and choppers will ruin it",
                    0.816
            ),
            (
                    "If requested by Client, Company may assist Client with activation of CisionIDs for paid retargeting campaigns via Company's third-party partner. If elected, this will be noted on Client's Order Form and / or SOW.If Client requests, Company may also provide the Audience resulting from Audience Segment Services to Client via Client's Data Management Platform (\"DMP\") or Demand Side Platform (\"DSP\"). In such case, Client will (i) promptly identify and provide Company with contact information for Client's DMP or DSP, and (ii) use the Audience Segment Services solely for Client's internal business purposes and in accordance with applicable Privacy Laws. In addition to the restrictions set forth in Section 5.4(C) above, Client agrees that it will not, and will not permit any other party to: (1) use the Audience(s) for or on behalf of any third party; or (2) provide any third party, other than Client's DMP or DSP, access to the Audience or information, materials or Documentation related to the Audience.Upon termination or expiration of this Agreement for any reason, Client will promptly delete the Audience and all data related to or derived from the Audience Segment Services, including that held by Client's DMP or DSP. \"Privacy Laws\" mean all laws, self- regulatory principles and codes of conduct governing the receipt, collection, compilation, use, storage, processing, sharing, safeguarding, security, disclosure or transfer of personal information, including those issued by the Network Advertising Initiative and the Digital Advertising Alliance.",
                    "If requested by Client, Company may assist Client with activation of IDs for paid retargeting campaigns via Company's third-party partner. If elected, this will be noted on Client's Order Form and / or SOW.If Client requests, Company may also provide the Audience resulting from Audience Segment Services to Client via Client's Data Management Platform or Demand Side Platform. In such case, Client will (i) promptly identify and provide Company with contact information for Client's DMP or DSP, and (ii) use the Audience Segment Services solely for Client's internal business purposes and in accordance with applicable Privacy Laws. In addition to the restrictions set forth in Section 5.4(C) above, Client agrees that it will not, and will not permit any other party to: (1) use the Audience(s) for or on behalf of any third party; or (2) provide any third party, other than Client's DMP or DSP, access to the Audience or information, materials or Documentation related to the Audience.Upon termination or expiration of this Agreement for any reason, Client will promptly delete the Audience and all data related to or derived from the Audience Segment Services, including that held by Client's DMP or DSP. \"Privacy Laws\" mean all laws, self- regulatory principles and codes of conduct governing the receipt, collection, compilation, use, storage, processing, sharing, safeguarding, security, disclosure or transfer of personal information, including those issued by the Network Advertising Initiative and the Digital Advertising Alliance.",
                    0.993
            )
        ]
    )
    def test_measure_string_distance(self, sent1: str, sent2: str, expected_distance: float):
        similarity_proximity = StringDistanceMeasurer()
        distance = similarity_proximity.measure_string_distance(sent1, sent2)

        assert pytest.approx(distance, ALLOWED_TOLERANCE) == expected_distance

    @pytest.mark.parametrize(
        "sent1, sent2, expected_distance",
        [
            (
                    "",
                    "SOME_VALUE",
                    0.0
            ),
            (
                    "SOME_VALUE",
                    "",
                    0.0
            ),
            (
                    "",
                    "",
                    0.0
            )
        ]
    )
    def test_measure_string_distance_empty_string(self, sent1: str, sent2: str, expected_distance: float):
        similarity_proximity = StringDistanceMeasurer()
        distance = similarity_proximity.measure_string_distance(sent1, sent2)

        assert distance == expected_distance

    @pytest.mark.parametrize(
        "sent1, sent2, expected_distance",
        [
            (
                    "SOME_VALUE",
                    "SOME_VALUE",
                    1.0
            ),
        ]
    )
    def test_measure_string_distance_same_string(self, sent1: str, sent2: str, expected_distance: float):
        similarity_proximity = StringDistanceMeasurer()
        distance = similarity_proximity.measure_string_distance(sent1, sent2)

        assert distance == expected_distance

