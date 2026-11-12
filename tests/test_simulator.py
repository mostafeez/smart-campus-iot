from src.simulator import create_initial_state, get_energy_summary, tick_simulation

def test_initial_state_has_expected_modules():
    state = create_initial_state()
    assert len(state["rooms"]) == 8
    assert len(state["parking"]) == 20
    assert "alerts" in state

def test_energy_saving_is_calculated():
    state = create_initial_state()
    state["baseline_kw"] = 100
    state["current_kw"] = 65
    assert get_energy_summary(state)["saving_pct"] == 35
    assert get_energy_summary(state)["saved_kw"] == 35

def test_simulation_keeps_power_non_negative():
    state = create_initial_state()
    tick_simulation(state)
    assert state["current_kw"] >= 0
    assert all(room["power_kw"] >= 0 for room in state["rooms"])
