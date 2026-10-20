import { z } from 'zod';

/** Family budgets are separate from a minor's personal cash. All money is
 * stored in pence. Optional v1 fields preserve old LIVEIT saves. */
export const HouseholdSchema = z
  .object({
    home: z.enum(['family_home', 'rented_flat', 'owned_home']),
    balancePence: z.number().int().min(-100000000).max(100000000),
    incomePence: z.number().int().min(0).max(10000000),
    expensesPence: z.number().int().min(0).max(10000000),
    dependents: z.number().int().min(0).max(20),
    lastSettledMonth: z.number().int().min(0),
    arrearsMonths: z.number().int().min(0).max(1200),
  })
  .strict();
export type Household = z.infer<typeof HouseholdSchema>;

export const SchoolSchema = z
  .object({
    phase: z.enum(['not_started', 'primary', 'secondary', 'graduated']),
    grade: z.number().int().min(0).max(100),
    attendance: z.number().int().min(0).max(100),
    engagement: z.number().int().min(0).max(100),
    discipline: z.number().int().min(0).max(100),
    studySessions: z.number().int().min(0).max(10000),
    club: z.enum(['science', 'arts', 'music', 'sports']).nullable(),
    lastTermMonth: z.number().int().min(0),
    graduatedWith: z.number().int().min(0).max(100).nullable(),
  })
  .strict();
export type School = z.infer<typeof SchoolSchema>;
