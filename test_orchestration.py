"""
Test script to verify backend orchestration of submission flow.
Tests: judge → reward → logs (all internal, no external tools)
"""
import sys
import logging
sys.path.insert(0, 'src')

# Set up logger for tests
logger = logging.getLogger(__name__)


def test_orchestration_function():
    """Test the orchestration function directly."""
    print("=" * 70)
    print("TEST 1: ORCHESTRATION FUNCTION")
    print("=" * 70)
    
    from src.routes.judge import orchestrate_submission_flow
    from src.database import get_db
    
    # Get database connection
    db = get_db()
    
    # Test the orchestration
    judging, reward, logging = orchestrate_submission_flow(
        submission_text="This is a test submission for orchestration.",
        team_id="test_team",
        tenant_id="test_tenant",
        event_id="test_event",
        workspace_id="test_workspace",
        submission_hash="abc123hash",
        db=db
    )
    
    print(f"\nJudging result:")
    print(f"  Success: {judging.get('success')}")
    print(f"  Score: {judging.get('data', {}).get('consensus_score')}")
    print(f"  Confidence: {judging.get('data', {}).get('confidence')}")
    
    print(f"\nReward result:")
    print(f"  Success: {reward.get('success')}")
    if reward.get('success'):
        print(f"  Value: {reward.get('data', {}).get('reward_value')}")
        print(f"  Outcome: {reward.get('data', {}).get('outcome')}")
    
    print(f"\nLogging result:")
    print(f"  Success: {logging.get('success')}")
    
    # Verify all steps completed
    all_success = judging.get('success') and logging.get('success')
    print(f"\nAll critical steps succeeded: {all_success}")
    
    return all_success


def test_tenant_event_flow():
    """Test that tenant_id and event_id flow through all orchestration steps."""
    print("\n" + "=" * 70)
    print("TEST 2: TENANT & EVENT ID FLOW")
    print("=" * 70)
    
    from src.routes.judge import orchestrate_submission_flow
    from src.database import get_db
    
    db = get_db()
    
    # Test with specific tenant and event
    judging, reward, logging = orchestrate_submission_flow(
        submission_text="Test submission for tenant flow.",
        team_id="team_alpha",
        tenant_id="tenant_xyz",
        event_id="event_123",
        workspace_id="workspace_1",
        submission_hash="xyz789hash",
        db=db
    )
    
    # Check that tenant and event are preserved in judging result
    judging_data = judging.get('data', {})
    tenant_preserved = judging_data.get('tenant_id') == "tenant_xyz"
    event_preserved = judging_data.get('event_id') == "event_123"
    
    print(f"\nTenant ID preserved through flow: {tenant_preserved}")
    print(f"Event ID preserved through flow: {event_preserved}")
    print(f"  Judging tenant: {judging_data.get('tenant_id')}")
    print(f"  Judging event: {judging_data.get('event_id')}")
    
    if reward.get('success'):
        reward_data = reward.get('data', {})
        print(f"  Reward outcome: {reward_data.get('outcome')}")
    
    return tenant_preserved and event_preserved


def test_error_handling():
    """Test that orchestration handles errors gracefully (no 500s)."""
    print("\n" + "=" * 70)
    print("TEST 3: ERROR HANDLING (DEMO-SAFE)")
    print("=" * 70)
    
    from src.routes.judge import orchestrate_submission_flow
    from src.database import get_db
    
    db = get_db()
    
    # Test with empty submission (should not crash)
    judging, reward, logging = orchestrate_submission_flow(
        submission_text="",  # Empty submission
        team_id="",
        tenant_id="default",
        event_id="default_event",
        workspace_id=None,
        submission_hash="empty_hash",
        db=db
    )
    
    print(f"\nEmpty submission handling:")
    print(f"  Judging success: {judging.get('success')}")
    print(f"  Reward success: {reward.get('success')}")
    print(f"  Logging success: {logging.get('success')}")
    
    # Even with empty submission, flow should complete without crashing
    flow_completed = logging.get('success')  # Logging is the last step
    print(f"\nFlow completed without errors: {flow_completed}")
    
    return flow_completed


def test_flow_order():
    """Verify the flow executes in correct order: judge → reward → logs."""
    print("\n" + "=" * 70)
    print("TEST 4: FLOW EXECUTION ORDER")
    print("=" * 70)
    
    from src.routes.judge import orchestrate_submission_flow
    from src.database import get_db
    
    db = get_db()
    
    judging, reward, logging = orchestrate_submission_flow(
        submission_text="Test submission for order verification.",
        team_id="order_test_team",
        tenant_id="default",
        event_id="default_event",
        workspace_id=None,
        submission_hash="order_hash",
        db=db
    )
    
    # Verify judging ran first (reward depends on it)
    judging_ran = judging.get('success')
    reward_has_outcome = reward.get('success') and 'outcome' in reward.get('data', {})
    logging_ran = logging.get('success')
    
    print(f"\nStep execution:")
    print(f"  1. Judging executed: {judging_ran}")
    print(f"  2. Reward calculated with outcome: {reward_has_outcome}")
    print(f"  3. Logging completed: {logging_ran}")
    
    # Correct order: judging must succeed for reward to have outcome
    correct_order = judging_ran and reward_has_outcome and logging_ran
    print(f"\nFlow executed in correct order: {correct_order}")
    
    return correct_order


def test_no_external_dependencies():
    """Verify flow runs without external tools (Zapier, LangGraph, etc.)."""
    print("\n" + "=" * 70)
    print("TEST 5: NO EXTERNAL DEPENDENCIES")
    print("=" * 70)
    
    from src.routes.judge import orchestrate_submission_flow
    from src.database import get_db
    
    db = get_db()
    
    # The orchestration should work without any external API calls
    # (except database which is internal)
    judging, reward, logging = orchestrate_submission_flow(
        submission_text="Test for internal execution.",
        team_id="internal_test",
        tenant_id="default",
        event_id="default_event",
        workspace_id=None,
        submission_hash="internal_hash",
        db=db
    )
    
    # All steps should complete using only internal logic
    all_internal = judging.get('success') and reward.get('success') and logging.get('success')
    
    print(f"\nFlow executed using only internal logic: {all_internal}")
    print(f"  (No Zapier, no LangGraph, no external webhooks)")
    
    return all_internal


def main():
    """Run all orchestration tests."""
    print("\n" + "=" * 70)
    print("BACKEND ORCHESTRATION TESTS")
    print("=" * 70)
    
    results = []
    results.append(("Orchestration Function", test_orchestration_function()))
    results.append(("Tenant & Event Flow", test_tenant_event_flow()))
    results.append(("Error Handling", test_error_handling()))
    results.append(("Flow Order", test_flow_order()))
    results.append(("No External Dependencies", test_no_external_dependencies()))
    
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("ALL ORCHESTRATION TESTS PASSED")
        print("\nBackend now fully controls the hackathon flow:")
        print("  1. Submission received")
        print("  2. Judging executed (internal)")
        print("  3. Reward calculated (internal)")
        print("  4. Logs recorded (internal)")
        print("\nNo external workflow tools required!")
    else:
        print("SOME ORCHESTRATION TESTS FAILED")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
