from legal_mask.detectors.keyword_matcher import KeywordMatcher


def test_detect_judge():
    matcher = KeywordMatcher()
    results = matcher.detect("审判长：王建国")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "judge"


def test_detect_clerk():
    matcher = KeywordMatcher()
    results = matcher.detect("书记员：刘伟")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "clerk"


def test_detect_assistant():
    matcher = KeywordMatcher()
    results = matcher.detect("法官助理：陈芳")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "judge_assistant"


def test_detect_court():
    matcher = KeywordMatcher()
    results = matcher.detect("北京市第一中级人民法院")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "court_name"


def test_detect_multiple_in_text():
    matcher = KeywordMatcher()
    text = "审判长：王建国，审判员：陈芳，法官助理：刘伟，书记员：赵丽"
    results = matcher.detect(text)
    assert len(results) == 4


def test_detect_all_judge_types():
    matcher = KeywordMatcher()
    results = matcher.detect("审判长 张三；审判员 李四；代理审判员 王五；人民陪审员 赵六")
    assert len(results) == 4


def test_no_matches():
    matcher = KeywordMatcher()
    results = matcher.detect("这是一个普通的测试文本")
    assert len(results) == 0
