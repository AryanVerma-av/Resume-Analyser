export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

export type ApplicationStatus =
  | 'applied'
  | 'reviewing'
  | 'interviewing'
  | 'offered'
  | 'rejected';

export type AnalysisStatus =
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed';

export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          full_name: string | null;
          email: string | null;
          profile_picture: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          full_name?: string | null;
          email?: string | null;
          profile_picture?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          full_name?: string | null;
          email?: string | null;
          profile_picture?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'profiles_id_fkey';
            columns: ['id'];
            isOneToOne: true;
            referencedRelation: 'users';
            referencedColumns: ['id'];
          }
        ];
      };
      resumes: {
        Row: {
          id: string;
          user_id: string;
          file_name: string;
          file_path: string;
          file_url: string | null;
          extracted_text: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          file_name: string;
          file_path: string;
          file_url?: string | null;
          extracted_text?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          file_name?: string;
          file_path?: string;
          file_url?: string | null;
          extracted_text?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'resumes_user_id_fkey';
            columns: ['user_id'];
            isOneToOne: false;
            referencedRelation: 'profiles';
            referencedColumns: ['id'];
          }
        ];
      };
      resume_analyses: {
        Row: {
          id: string;
          resume_id: string;
          overall_score: number | null;
          ats_score: number | null;
          skills_score: number | null;
          experience_score: number | null;
          education_score: number | null;
          strengths: Json;
          weaknesses: Json;
          missing_skills: Json;
          recommendations: Json;
          analysis_status: AnalysisStatus;
          created_at: string;
        };
        Insert: {
          id?: string;
          resume_id: string;
          overall_score?: number | null;
          ats_score?: number | null;
          skills_score?: number | null;
          experience_score?: number | null;
          education_score?: number | null;
          strengths?: Json;
          weaknesses?: Json;
          missing_skills?: Json;
          recommendations?: Json;
          analysis_status?: AnalysisStatus;
          created_at?: string;
        };
        Update: {
          id?: string;
          resume_id?: string;
          overall_score?: number | null;
          ats_score?: number | null;
          skills_score?: number | null;
          experience_score?: number | null;
          education_score?: number | null;
          strengths?: Json;
          weaknesses?: Json;
          missing_skills?: Json;
          recommendations?: Json;
          analysis_status?: AnalysisStatus;
          created_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'resume_analyses_resume_id_fkey';
            columns: ['resume_id'];
            isOneToOne: false;
            referencedRelation: 'resumes';
            referencedColumns: ['id'];
          }
        ];
      };
      jobs: {
        Row: {
          id: string;
          title: string;
          company: string;
          location: string | null;
          description: string | null;
          requirements: Json;
          skills: Json;
          salary: string | null;
          job_url: string | null;
          source: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          title: string;
          company: string;
          location?: string | null;
          description?: string | null;
          requirements?: Json;
          skills?: Json;
          salary?: string | null;
          job_url?: string | null;
          source?: string | null;
          created_at?: string;
        };
        Update: {
          id?: string;
          title?: string;
          company?: string;
          location?: string | null;
          description?: string | null;
          requirements?: Json;
          skills?: Json;
          salary?: string | null;
          job_url?: string | null;
          source?: string | null;
          created_at?: string;
        };
        Relationships: [];
      };
      saved_jobs: {
        Row: {
          id: string;
          user_id: string;
          job_id: string;
          created_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          job_id: string;
          created_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          job_id?: string;
          created_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'saved_jobs_job_id_fkey';
            columns: ['job_id'];
            isOneToOne: false;
            referencedRelation: 'jobs';
            referencedColumns: ['id'];
          },
          {
            foreignKeyName: 'saved_jobs_user_id_fkey';
            columns: ['user_id'];
            isOneToOne: false;
            referencedRelation: 'profiles';
            referencedColumns: ['id'];
          }
        ];
      };
      job_applications: {
        Row: {
          id: string;
          user_id: string;
          job_id: string;
          status: ApplicationStatus;
          applied_at: string;
          notes: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          job_id: string;
          status?: ApplicationStatus;
          applied_at?: string;
          notes?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          job_id?: string;
          status?: ApplicationStatus;
          applied_at?: string;
          notes?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Relationships: [
          {
            foreignKeyName: 'job_applications_job_id_fkey';
            columns: ['job_id'];
            isOneToOne: false;
            referencedRelation: 'jobs';
            referencedColumns: ['id'];
          },
          {
            foreignKeyName: 'job_applications_user_id_fkey';
            columns: ['user_id'];
            isOneToOne: false;
            referencedRelation: 'profiles';
            referencedColumns: ['id'];
          }
        ];
      };
    };
    Views: Record<string, never>;
    Functions: Record<string, never>;
    Enums: {
      application_status: ApplicationStatus;
      analysis_status: AnalysisStatus;
    };
    CompositeTypes: Record<string, never>;
  };
}

// Strongly-typed convenient helper aliases
export type Profile = Database['public']['Tables']['profiles']['Row'];
export type Resume = Database['public']['Tables']['resumes']['Row'];
export type ResumeAnalysis = Database['public']['Tables']['resume_analyses']['Row'];
export type Job = Database['public']['Tables']['jobs']['Row'];
export type SavedJob = Database['public']['Tables']['saved_jobs']['Row'];
export type JobApplication = Database['public']['Tables']['job_applications']['Row'];

// Domain structure for AI recommendations & breakdown
export interface AnalysisRecommendations {
  action_steps?: string[];
  course_suggestions?: string[];
  curriculum_track?: string;
  interview_prep_questions?: string[];
}
