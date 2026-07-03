from legal_mask.detectors.rule_engine import RuleEngine


def test_detect_id_card():
    engine = RuleEngine()
    results = engine.detect("身份证号110101199003151234。")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "id_card"
    assert results[0].text == "110101199003151234"


def test_detect_phone():
    engine = RuleEngine()
    results = engine.detect("电话13800138000。")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "phone"


def test_detect_case_number():
    engine = RuleEngine()
    results = engine.detect("案号（2024）京01民初123号。")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "case_number"


def test_detect_credit_code():
    engine = RuleEngine()
    results = engine.detect("信用代码91110000MA12345678。")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "credit_code"


def test_detect_email():
    engine = RuleEngine()
    results = engine.detect("邮箱test@example.com。")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "email"


def test_detect_multiple():
    engine = RuleEngine()
    text = "张三身份证110101199003151234，电话13800138000"
    results = engine.detect(text)
    assert len(results) == 2


def test_detect_no_false_positives():
    engine = RuleEngine()
    results = engine.detect("这是一个测试文本，不包含敏感信息。")
    assert len(results) == 0


def test_detect_bank_account():
    engine = RuleEngine()
    results = engine.detect("银行卡号6222021234567890123")
    assert len(results) == 1
    assert results[0].sensitive_type.value == "bank_account"
