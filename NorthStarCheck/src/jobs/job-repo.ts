import { randomUUID } from 'node:crypto';
import type { HiringTeamMember, Job, JobSource, JobStatus } from '../roles/types.js';

const jobs = new Map<string, Job>();
const members: HiringTeamMember[] = [];

export function clearStores(): void {
  jobs.clear();
  members.length = 0;
}

export function createJobRecord(
  tenantId: string,
  createdByUserId: string,
  source: JobSource,
): Job {
  const job: Job = {
    jobId: randomUUID(),
    tenantId,
    status: 'open',
    createdByUserId,
    source,
  };
  jobs.set(job.jobId, job);
  return job;
}

export function getJob(jobId: string): Job | undefined {
  return jobs.get(jobId);
}

export function deleteJobRecord(jobId: string): boolean {
  return jobs.delete(jobId);
}

export function setJobStatus(jobId: string, status: JobStatus): Job | undefined {
  const job = jobs.get(jobId);
  if (!job) return undefined;
  job.status = status;
  return job;
}

export function addHiringTeamMember(member: HiringTeamMember): void {
  members.push({ ...member });
}

export function getMembersForJob(jobId: string): HiringTeamMember[] {
  return members.filter((m) => m.jobId === jobId);
}

export function getMembersForUserOnJob(jobId: string, userId: string): HiringTeamMember[] {
  return members.filter((m) => m.jobId === jobId && m.userId === userId);
}

export function listAllMembers(): HiringTeamMember[] {
  return [...members];
}
