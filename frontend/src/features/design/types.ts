export interface Screen {
  name: string
  description: string
}

export interface DesignSpec {
  user_journey: string[]
  screens: Screen[]
  navigation: string[]
  ui_states: string[]
  components: string[]
  apis: string[]
  data_model: string[]
  ai_workflow: string[]
  tech_decisions: string[]
}

export interface DesignResponse {
  mvp_version: number
  created_at: string
  design: DesignSpec
}
