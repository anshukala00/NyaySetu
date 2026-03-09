export interface User {
  id: string
  email: string
  role: 'CITIZEN' | 'JUDGE'
}

export interface Case {
  id: string
  title: string
  description: string
  status: 'FILED' | 'IN_REVIEW' | 'HEARING_SCHEDULED'
  user_id: string
  judge_id: string | null
  priority: 'HIGH' | 'REGULAR' | null
  ai_summary: string | null
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user_id: string
  role: 'CITIZEN' | 'JUDGE'
}

export interface PrecedentResult {
  case_name: string
  summary: string
  relevance_score: number
}
