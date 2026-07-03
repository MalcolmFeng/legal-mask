export type SensitiveType =
  | 'person_name' | 'id_card' | 'phone' | 'case_number'
  | 'court_name' | 'company_name' | 'credit_code' | 'address'
  | 'email' | 'bank_account' | 'judge' | 'judge_assistant'
  | 'clerk' | 'custom'

export type AnnotationStatus = 'pending' | 'confirmed' | 'ignored' | 'modified'

export interface Annotation {
  id: string
  doc_id: string
  sensitive_type: SensitiveType
  start: number
  end: number
  text: string
  confidence: number
  source: string
  status: AnnotationStatus
  note: string
}

export interface DocumentInfo {
  id: string
  filename: string
  file_type: string
  content?: string
  content_length?: number
  annotations?: Annotation[]
  annotation_count?: number
}

export const SENSITIVE_TYPE_LABELS: Record<string, string> = {
  person_name: '姓名',
  id_card: '身份证号',
  phone: '手机号',
  case_number: '案号',
  court_name: '法院名称',
  company_name: '企业名称',
  credit_code: '统一社会信用代码',
  address: '地址',
  email: '邮箱',
  bank_account: '银行账户',
  judge: '审判法官',
  judge_assistant: '法官助理',
  clerk: '书记员',
  custom: '自定义',
}

export const SENSITIVE_TYPE_COLORS: Record<string, string> = {
  person_name: '#FF6B6B',
  id_card: '#4ECDC4',
  phone: '#45B7D1',
  case_number: '#96CEB4',
  court_name: '#9B59B6',
  company_name: '#F39C12',
  credit_code: '#1ABC9C',
  address: '#E67E22',
  email: '#3498DB',
  bank_account: '#E74C3C',
  judge: '#8E44AD',
  judge_assistant: '#2C3E50',
  clerk: '#7F8C8D',
  custom: '#95A5A6',
}
