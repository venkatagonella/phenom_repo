import { Component } from '@angular/core';
import {
  JobCandidatePipelineComponent,
  JobPipelineStage,
} from './components/job-candidate-pipeline/job-candidate-pipeline.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [JobCandidatePipelineComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  jobTitle = 'Director of Platform Engineering';
  jobStatus = 'Draft';
  selectedStageId = 'active';

  stages: JobPipelineStage[] = [
    {
      id: 'leads',
      label: 'Leads',
      type: 'standard',
      candidateCount: 1,
      icon: '🪙',
    },
    {
      id: 'application-review',
      label: 'Application Review',
      type: 'standard',
      candidateCount: 0,
      icon: '📋',
    },
    {
      id: 'active',
      label: 'Active',
      type: 'standard',
      candidateCount: 6,
      icon: '💬',
    },
    {
      id: 'pending-offer',
      label: 'Pending Offer',
      type: 'standard',
      candidateCount: 0,
      icon: '📄',
    },
    {
      id: 'hired',
      label: 'Hired',
      type: 'standard',
      candidateCount: 0,
      icon: '✅',
    },
    {
      id: 'archived',
      label: 'Archived',
      type: 'standard',
      candidateCount: 17,
      icon: '📦',
    },
  ];

  onStageChange(stage: JobPipelineStage): void {
    this.selectedStageId = stage.id;
  }
}
