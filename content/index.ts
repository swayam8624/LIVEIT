import { parseStory } from '@living/story-schema';
const memory = (fact: string, text: string) => ({
  operation: 'add_memory' as const,
  target: 'amelia',
  fact,
  text,
});
const trust = (value: number) => ({
  operation: 'adjust_relationship' as const,
  target: 'amelia',
  value,
});
export const reunion = parseStory({
  schemaVersion: 1,
  id: 'official.the-space-between',
  version: 1,
  title: 'The Space Between',
  description:
    'An old friend. An unfinished conversation. Some things follow you to a new city.',
  compatibleWorlds: ['modern_life_v1'],
  minAge: 18,
  permissions: { relationshipTargets: ['amelia'], memoryTargets: ['amelia'] },
  entry: 'arrival',
  scenes: [
    {
      id: 'arrival',
      speaker: 'Amelia',
      mood: 'reflective',
      text: 'I kept almost calling you. And then a month became a year. Funny how that happens. I didn’t think you’d come.',
      ending: false,
      choices: [
        {
          id: 'apologize',
          label: '“I should have called. I’m sorry.”',
          next: 'honesty',
          conditions: [],
          effects: [
            trust(12),
            memory(
              'apologized',
              'You took responsibility for the silence between you and Amelia.',
            ),
          ],
        },
        {
          id: 'listen',
          label: '“I’m here now. Tell me how you’ve been.”',
          next: 'listening',
          conditions: [],
          effects: [
            trust(6),
            memory(
              'listened',
              'You made space for Amelia to tell her side of the story.',
            ),
          ],
        },
        {
          id: 'guarded',
          label: '“You stopped calling too.”',
          next: 'distance',
          conditions: [],
          effects: [
            trust(-8),
            memory(
              'guarded',
              'Old hurt resurfaced when you met Amelia at the café.',
            ),
          ],
        },
      ],
    },
    {
      id: 'honesty',
      speaker: 'Amelia',
      mood: 'warm',
      text: 'Thank you for saying that. I thought I’d rehearsed this conversation a hundred times, but I never got past the first sentence. What happened to us?',
      ending: false,
      choices: [
        {
          id: 'truth',
          label: '“I was afraid I’d let you down.”',
          next: 'reconnected',
          conditions: [],
          effects: [
            trust(10),
            memory(
              'honest_reunion',
              'You told Amelia the truth. The friendship has a way forward.',
            ),
          ],
        },
        {
          id: 'coffee',
          label: '“Can we start with coffee, and take our time?”',
          next: 'slow',
          conditions: [],
          effects: [
            trust(5),
            memory(
              'coffee_again',
              'You and Amelia agreed to rebuild slowly, one coffee at a time.',
            ),
          ],
        },
      ],
    },
    {
      id: 'listening',
      speaker: 'Amelia',
      mood: 'reflective',
      text: 'I’m opening a little bookshop. Terrifying, honestly. I wanted you to hear it from me. There’s a launch next week, if you want to come.',
      ending: false,
      choices: [
        {
          id: 'support',
          label: '“I wouldn’t miss it.”',
          next: 'reconnected',
          conditions: [],
          effects: [
            trust(10),
            memory(
              'bookshop_invitation',
              'Amelia invited you to her bookshop opening. You promised to be there.',
            ),
          ],
        },
        {
          id: 'explain',
          label: '“Before that, I owe you an explanation.”',
          next: 'honesty',
          conditions: [],
          effects: [trust(4)],
        },
      ],
    },
    {
      id: 'distance',
      speaker: 'Amelia',
      mood: 'tense',
      text: 'You’re right. I did. I guess I hoped one of us would be brave enough to break the silence. We can keep score, or we can try something else.',
      ending: false,
      choices: [
        {
          id: 'repair',
          label: '“I don’t want to keep score anymore.”',
          next: 'slow',
          conditions: [],
          effects: [
            trust(8),
            memory(
              'chose_repair',
              'Despite a difficult start, you chose to give your friendship another chance.',
            ),
          ],
        },
        {
          id: 'leave',
          label: '“Maybe we both need more time.”',
          next: 'apart',
          conditions: [],
          effects: [
            memory(
              'needed_space',
              'You and Amelia parted kindly, but the distance remains.',
            ),
          ],
        },
      ],
    },
    {
      id: 'reconnected',
      speaker: 'Amelia',
      mood: 'warm',
      text: 'Then let’s not wait another year. Outside, the rain has stopped. For the first time since moving here, this city feels a little more like home.',
      ending: true,
      choices: [],
    },
    {
      id: 'slow',
      speaker: 'Amelia',
      mood: 'warm',
      text: 'One coffee at a time. I can do that. She smiles, just a little. Some beginnings are quiet enough that you almost miss them.',
      ending: true,
      choices: [],
    },
    {
      id: 'apart',
      speaker: 'Amelia',
      mood: 'reflective',
      text: 'Take care of yourself, okay? Her cup is still half full when you leave. Not every reunion is a return. Sometimes it’s a place to pause.',
      ending: true,
      choices: [],
    },
  ],
});
