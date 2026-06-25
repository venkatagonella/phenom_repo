import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import {
  PxViewGroupComponent,
  PxViewGroupItem,
} from '../../pds/public-api';

export interface JobPipelineStage extends PxViewGroupItem {
  candidateCount: number;
}

@Component({
  selector: 'app-job-candidate-pipeline',
  standalone: true,
  imports: [CommonModule, PxViewGroupComponent],
  templateUrl: './job-candidate-pipeline.component.html',
  styleUrl: './job-candidate-pipeline.component.scss',
})
export class JobCandidatePipelineComponent {
  @Input({ required: true }) jobTitle = '';
  @Input() jobStatus = 'Draft';
  @Input() stages: JobPipelineStage[] = [];
  @Input() selectedStageId = '';

  @Output() stageChange = new EventEmitter<JobPipelineStage>();

  get pipelineViews(): PxViewGroupItem[] {
    return this.stages.map((stage) => ({
      ...stage,
      subtitle: this.formatCandidateCount(stage.candidateCount),
    }));
  }

  onStageSelected(view: PxViewGroupItem): void {
    const stage = this.stages.find((item) => item.id === view.id);
    if (stage) {
      this.selectedStageId = stage.id;
      this.stageChange.emit(stage);
    }
  }

  private formatCandidateCount(count: number): string {
    const label = count === 1 ? 'Candidate' : 'Candidates';
    return `${count} ${label}`;
  }
}
