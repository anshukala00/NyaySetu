import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { LoginPage } from '../pages/LoginPage';
import { JudgeDashboard } from '../pages/JudgeDashboard';
import { authService, caseService, precedentService } from '../services/api';

/**
 * E2E Test: Complete Judge Workflow
 * 
 * This test verifies the complete judge workflow:
 * 1. Login with judge credentials
 * 2. View all cases in the system
 * 3. Select a case and generate AI summary
 * 4. Search for precedents
 * 
 * Prerequisites:
 * - Backend API must be running on http://localhost:8000
 * - Database must have test data (17 cases)
 * - Test judge account: judge1@example.com / password123
 */

describe('E2E: Complete Judge Workflow', () => {
  const TEST_JUDGE_EMAIL = 'judge1@example.com';
  const TEST_JUDGE_PASSWORD = 'password123';
  
  let authToken: string;
  let testCaseId: string;

  beforeAll(async () => {
    // Clear any existing auth state
    localStorage.clear();
  });

  afterAll(() => {
    // Cleanup
    localStorage.clear();
  });

  it('should complete the full judge workflow: login → view cases → generate summary → search precedents', async () => {
    const user = userEvent.setup();

    // ============================================
    // STEP 1: Login as Judge
    // ============================================
    console.log('Step 1: Logging in as judge...');
    
    const loginResponse = await authService.login(TEST_JUDGE_EMAIL, TEST_JUDGE_PASSWORD);
    
    expect(loginResponse).toBeDefined();
    expect(loginResponse.access_token).toBeDefined();
    expect(loginResponse.role).toBe('JUDGE');
    expect(loginResponse.user_id).toBeDefined();
    
    // Store auth token
    authToken = loginResponse.access_token;
    localStorage.setItem('access_token', authToken);
    localStorage.setItem('user_id', loginResponse.user_id);
    localStorage.setItem('user_role', loginResponse.role);
    
    console.log('✓ Login successful');

    // ============================================
    // STEP 2: View All Cases
    // ============================================
    console.log('Step 2: Fetching all cases...');
    
    const cases = await caseService.getCases(1, 50);
    
    expect(cases).toBeDefined();
    expect(Array.isArray(cases)).toBe(true);
    expect(cases.length).toBeGreaterThan(0);
    
    // Verify we can see cases from different citizens (judge sees all)
    console.log(`✓ Retrieved ${cases.length} cases`);
    
    // Select the first case for testing
    testCaseId = cases[0].id;
    expect(testCaseId).toBeDefined();
    
    console.log(`✓ Selected case ${testCaseId} for testing`);

    // ============================================
    // STEP 3: View Case Details
    // ============================================
    console.log('Step 3: Viewing case details...');
    
    const caseDetails = await caseService.getCaseById(testCaseId);
    
    expect(caseDetails).toBeDefined();
    expect(caseDetails.id).toBe(testCaseId);
    expect(caseDetails.title).toBeDefined();
    expect(caseDetails.description).toBeDefined();
    expect(caseDetails.status).toBeDefined();
    expect(caseDetails.priority).toBeDefined();
    
    console.log(`✓ Case details retrieved: "${caseDetails.title}"`);
    console.log(`  Status: ${caseDetails.status}, Priority: ${caseDetails.priority}`);

    // ============================================
    // STEP 4: Generate AI Summary
    // ============================================
    console.log('Step 4: Generating AI summary...');
    
    const summary = await caseService.generateSummary(testCaseId);
    
    expect(summary).toBeDefined();
    expect(typeof summary).toBe('string');
    expect(summary.length).toBeGreaterThan(0);
    expect(summary).toContain('[AI Generated Summary]');
    
    console.log(`✓ AI summary generated: "${summary.substring(0, 100)}..."`);

    // ============================================
    // STEP 5: Verify Summary is Stored
    // ============================================
    console.log('Step 5: Verifying summary is stored...');
    
    const updatedCase = await caseService.getCaseById(testCaseId);
    
    expect(updatedCase.ai_summary).toBeDefined();
    expect(updatedCase.ai_summary).toBe(summary);
    
    console.log('✓ Summary successfully stored in case record');

    // ============================================
    // STEP 6: Search for Precedents
    // ============================================
    console.log('Step 6: Searching for precedents...');
    
    // Use keywords from the case description for search
    const searchQuery = 'property dispute';
    const precedents = await precedentService.search(searchQuery, 5);
    
    expect(precedents).toBeDefined();
    expect(Array.isArray(precedents)).toBe(true);
    expect(precedents.length).toBeGreaterThan(0);
    expect(precedents.length).toBeLessThanOrEqual(5);
    
    // Verify precedent structure
    const firstPrecedent = precedents[0];
    expect(firstPrecedent.case_name).toBeDefined();
    expect(firstPrecedent.summary).toBeDefined();
    expect(firstPrecedent.relevance_score).toBeDefined();
    expect(typeof firstPrecedent.relevance_score).toBe('number');
    
    console.log(`✓ Found ${precedents.length} relevant precedents`);
    console.log(`  Top result: "${firstPrecedent.case_name}" (score: ${firstPrecedent.relevance_score})`);

    // ============================================
    // STEP 7: Verify Precedents are Ranked
    // ============================================
    console.log('Step 7: Verifying precedents are ranked by relevance...');
    
    // Check that precedents are sorted by relevance score (descending)
    for (let i = 0; i < precedents.length - 1; i++) {
      expect(precedents[i].relevance_score).toBeGreaterThanOrEqual(precedents[i + 1].relevance_score);
    }
    
    console.log('✓ Precedents are correctly ranked by relevance score');

    // ============================================
    // WORKFLOW COMPLETE
    // ============================================
    console.log('\n✅ Complete judge workflow test PASSED');
    console.log('Summary:');
    console.log(`  - Logged in as: ${TEST_JUDGE_EMAIL}`);
    console.log(`  - Viewed ${cases.length} cases`);
    console.log(`  - Generated summary for case: ${testCaseId}`);
    console.log(`  - Found ${precedents.length} relevant precedents`);
  });

  it('should verify judge can access cases from different citizens', async () => {
    console.log('\nVerifying judge authorization...');
    
    // Login as judge
    const loginResponse = await authService.login(TEST_JUDGE_EMAIL, TEST_JUDGE_PASSWORD);
    localStorage.setItem('access_token', loginResponse.access_token);
    
    // Get all cases
    const cases = await caseService.getCases(1, 50);
    
    // Verify we have cases from multiple citizens
    const uniqueCitizens = new Set(cases.map((c: any) => c.user_id));
    
    expect(uniqueCitizens.size).toBeGreaterThan(1);
    console.log(`✓ Judge can access cases from ${uniqueCitizens.size} different citizens`);
  });

  it('should handle errors gracefully when case not found', async () => {
    console.log('\nTesting error handling...');
    
    // Login as judge
    const loginResponse = await authService.login(TEST_JUDGE_EMAIL, TEST_JUDGE_PASSWORD);
    localStorage.setItem('access_token', loginResponse.access_token);
    
    // Try to access non-existent case
    const invalidCaseId = '00000000-0000-0000-0000-000000000000';
    
    await expect(caseService.getCaseById(invalidCaseId)).rejects.toThrow();
    console.log('✓ Error handling works correctly for invalid case ID');
  });

  it('should handle empty precedent search results', async () => {
    console.log('\nTesting precedent search with no results...');
    
    // Login as judge
    const loginResponse = await authService.login(TEST_JUDGE_EMAIL, TEST_JUDGE_PASSWORD);
    localStorage.setItem('access_token', loginResponse.access_token);
    
    // Search with very specific query that won't match
    const precedents = await precedentService.search('xyzabc123nonexistent', 5);
    
    expect(precedents).toBeDefined();
    expect(Array.isArray(precedents)).toBe(true);
    // May return empty array or low-relevance results
    console.log(`✓ Precedent search handled query with ${precedents.length} results`);
  });
});
