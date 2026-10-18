import React, { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import {
  ageUp,
  applyForJob,
  attendJobInterview,
  requestPromotion,
  resignFromJob,
  CATALOG,
  portfolio,
  netWorth,
  buyAsset,
  sellAsset,
  investIndex,
  withdrawIndex,
  pendingLifeMoment,
  resolveLifeMoment,
} from '@living/simulation-core';
import type { World, CareerPath } from '@living/world-schema';
import { AvatarPortrait } from './AvatarPortrait';
import { gameTheme as t } from './gameTheme';

const GOODS = ['bicycle', 'car', 'flat', 'townhouse'] as const;
const ROLES: {
  field: Exclude<CareerPath, 'undecided'>;
  label: string;
  caption: string;
}[] = [
  {
    field: 'technology',
    label: 'Developer',
    caption: 'Systems, software and practical problem-solving',
  },
  {
    field: 'creative',
    label: 'Designer',
    caption: 'Visual arts, studios and creative projects',
  },
  {
    field: 'business',
    label: 'Business',
    caption: 'Trading, negotiations and enterprise',
  },
  {
    field: 'community',
    label: 'Community',
    caption: 'Local institutions and people-first work',
  },
];
function cash(pence: number) {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    maximumFractionDigits: 0,
  }).format(pence / 100);
}
export function LifeDashboard({
  world,
  onAction,
}: {
  world: World;
  onAction: (apply: (current: World) => World) => void;
}) {
  const [careerOpen, setCareerOpen] = useState(false);
  const [assetsOpen, setAssetsOpen] = useState(false);
  const age = Math.floor(world.player.ageDays / 365);
  const job = world.city?.employment;
  const last = world.history.at(-1);
  const moment = pendingLifeMoment(world);
  return (
    <View style={styles.shell}>
      <View style={styles.hero}>
        <View style={styles.heroPortrait}>
          <AvatarPortrait appearance={world.player.appearance} size={130} />
        </View>
        <View style={styles.heroContent}>
          <Text style={styles.eyebrow}>YOUR LIFE • AGE {age}</Text>
          <Text style={styles.name}>{world.player.name}</Text>
          <Text style={styles.tagline}>
            {job && job.stage !== 'applied'
              ? job.jobTitle
              : 'Your next chapter is waiting'}
          </Text>
          <View style={styles.stats}>
            <View style={styles.stat}>
              <Text style={styles.statLabel}>SAVINGS</Text>
              <Text style={styles.statValue}>{cash(world.player.money)}</Text>
            </View>
            <View style={styles.stat}>
              <Text style={styles.statLabel}>WELLBEING</Text>
              <Text style={styles.statValue}>{world.player.wellbeing}%</Text>
            </View>
            <View style={styles.stat}>
              <Text style={styles.statLabel}>EXPERIENCE</Text>
              <Text style={styles.statValue}>{world.player.skill}/100</Text>
            </View>
          </View>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel="Age up one year"
            onPress={() => onAction(ageUp)}
            disabled={Boolean(moment)}
            style={({ pressed }) => [
              styles.ageButton,
              pressed && styles.pressed,
              Boolean(moment) && { opacity: 0.45 },
            ]}
          >
            <View style={{ flex: 1, gap: 3 }}>
              <Text style={styles.ageButtonText}>
                {moment ? 'MAKE YOUR CHOICE FIRST' : `AGE UP  ➜  ${age + 1}`}
              </Text>
              <Text style={styles.ageButtonHint}>
                Advance one year • discover new life events
              </Text>
            </View>
            <Text style={styles.ageIcon}>✧</Text>
          </Pressable>
        </View>
      </View>
      {moment && (
        <View style={styles.momentCard}>
          <Text style={styles.momentLabel}>
            A MOMENT THAT COULD CHANGE YOUR LIFE
          </Text>
          <Text style={styles.momentTitle}>{moment.title}</Text>
          <Text style={styles.momentDescription}>{moment.situation}</Text>
          <View style={styles.jobs}>
            {moment.choices.map((choice) => (
              <Pressable
                key={choice.id}
                accessibilityRole="button"
                accessibilityLabel={choice.text}
                style={({ pressed }) => [
                  styles.momentChoice,
                  pressed && styles.pressed,
                ]}
                onPress={() => onAction((w) => resolveLifeMoment(w, choice.id))}
              >
                <Text style={styles.momentChoiceText}>{choice.text} ↗</Text>
              </Pressable>
            ))}
          </View>
          <Text style={styles.muted}>
            Your decision changes money, relationships, skills or wellbeing and
            stays in your life history.
          </Text>
        </View>
      )}
      {last && (
        <View style={styles.lifeReel}>
          <Text style={styles.eyebrow}>LATEST LIFE MOMENT</Text>
          <Text style={styles.reelText}>{last.text}</Text>
        </View>
      )}
      <View style={styles.careerArea}>
        <View style={styles.careerHeading}>
          <View style={{ flex: 1, gap: 4 }}>
            <Text style={styles.eyebrow}>CAREER</Text>
            <Text style={styles.careerTitle}>
              {job ? job.jobTitle : 'Find your place in the world.'}
            </Text>
            <Text style={styles.muted}>
              {job && job.stage !== 'applied'
                ? `${job.company} · ${cash(job.salaryAnnual)} / year · ${job.experience} workdays experience`
                : job
                  ? `${job.company} has invited you to interview.`
                  : 'Apply to an employer, interview, work and earn your promotions.'}
            </Text>
          </View>
        </View>
        {!job && (
          <Pressable
            accessibilityRole="button"
            onPress={() => setCareerOpen((v) => !v)}
            style={styles.careerButton}
          >
            <Text style={styles.buttonText}>
              {careerOpen ? 'Close job listings' : 'Search available jobs  ↗'}
            </Text>
          </Pressable>
        )}
        {careerOpen && !job && (
          <View style={styles.jobs}>
            {ROLES.map((role) => (
              <Pressable
                key={role.field}
                accessibilityRole="button"
                accessibilityLabel={'Apply for ' + role.label}
                onPress={() => {
                  onAction((w) => applyForJob(w, role.field));
                  setCareerOpen(false);
                }}
                style={({ pressed }) => [
                  styles.jobItem,
                  pressed && styles.pressed,
                ]}
              >
                <View style={{ flex: 1, gap: 3 }}>
                  <Text style={styles.jobTitle}>{role.label}</Text>
                  <Text style={styles.muted}>{role.caption}</Text>
                </View>
                <Text style={styles.actionMark}>APPLY ↗</Text>
              </Pressable>
            ))}
          </View>
        )}
        {job?.stage === 'applied' && (
          <Pressable
            accessibilityRole="button"
            accessibilityLabel="Attend job interview"
            onPress={() => onAction(attendJobInterview)}
            style={styles.careerButton}
          >
            <Text style={styles.buttonText}>Attend the interview ↗</Text>
          </Pressable>
        )}
        {job && job.stage !== 'applied' && (
          <View style={styles.careerButtons}>
            <Pressable
              accessibilityRole="button"
              accessibilityLabel="Request promotion"
              onPress={() => onAction(requestPromotion)}
              style={styles.careerButton}
            >
              <Text style={styles.buttonText}>Request promotion ↗</Text>
            </Pressable>
            <Pressable
              accessibilityRole="button"
              accessibilityLabel="Resign from job"
              onPress={() => onAction(resignFromJob)}
              style={styles.ghostButton}
            >
              <Text style={styles.muted}>Resign</Text>
            </Pressable>
          </View>
        )}
      </View>
      <View style={styles.careerArea}>
        <View style={styles.careerHeading}>
          <View style={{ flex: 1, gap: 4 }}>
            <Text style={styles.eyebrow}>ASSETS & INVESTMENTS</Text>
            <Text style={styles.careerTitle}>
              Net worth {cash(netWorth(world))}
            </Text>
            <Text style={styles.muted}>
              Cash {cash(world.player.money)} · Index{' '}
              {cash(portfolio(world).indexPence)} ·{' '}
              {portfolio(world).owned.length} owned assets
            </Text>
          </View>
        </View>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Open assets and investments"
          onPress={() => setAssetsOpen((v) => !v)}
          style={styles.careerButton}
        >
          <Text style={styles.buttonText}>
            {assetsOpen
              ? 'Close portfolio'
              : 'Manage assets and investments  ↗'}
          </Text>
        </Pressable>
        {assetsOpen && (
          <View style={styles.jobs}>
            <Text style={styles.muted}>
              Real purchases affect cash, yearly maintenance and resale value.
              The index uses a deterministic fictional market, not live trading.
            </Text>
            <View style={styles.careerButtons}>
              <Pressable
                accessibilityRole="button"
                accessibilityLabel="Invest 100 pounds"
                style={styles.careerButton}
                onPress={() => onAction((w) => investIndex(w, 10000))}
              >
                <Text style={styles.buttonText}>Invest £100</Text>
              </Pressable>
              <Pressable
                accessibilityRole="button"
                accessibilityLabel="Withdraw 100 pounds"
                style={styles.ghostButton}
                onPress={() => onAction((w) => withdrawIndex(w, 10000))}
              >
                <Text style={styles.muted}>Withdraw £100</Text>
              </Pressable>
            </View>
            {GOODS.map((id) => {
              const product = CATALOG[id];
              const owned = portfolio(world).owned.some(
                (asset) => asset.id === id,
              );
              return (
                <View key={id} style={styles.jobItem}>
                  <View style={{ flex: 1, gap: 3 }}>
                    <Text style={styles.jobTitle}>{product.label}</Text>
                    <Text style={styles.muted}>
                      Purchase {cash(product.price)} · Annual upkeep{' '}
                      {cash(product.annualUpkeep)}
                    </Text>
                  </View>
                  <Pressable
                    accessibilityRole="button"
                    accessibilityLabel={
                      owned ? 'Sell ' + product.label : 'Buy ' + product.label
                    }
                    onPress={() =>
                      onAction((w) =>
                        owned ? sellAsset(w, id) : buyAsset(w, id),
                      )
                    }
                    style={styles.ghostButton}
                  >
                    <Text style={styles.actionMark}>
                      {owned ? 'SELL' : 'BUY'} ↗
                    </Text>
                  </Pressable>
                </View>
              );
            })}
          </View>
        )}
      </View>
    </View>
  );
}
const styles = StyleSheet.create({
  shell: { gap: 12 },
  hero: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    backgroundColor: t.panel,
    borderColor: t.border,
    borderWidth: 1,
    borderRadius: 16,
    overflow: 'hidden',
  },
  heroPortrait: {
    flexGrow: 1,
    flexBasis: 138,
    minHeight: 184,
    backgroundColor: t.panelRaised,
    justifyContent: 'flex-end',
    paddingTop: 10,
  },
  heroContent: { flexGrow: 3, flexBasis: 225, padding: 16, gap: 10 },
  eyebrow: {
    fontFamily: t.font.hud,
    fontSize: 10,
    letterSpacing: 1.6,
    fontWeight: '800',
    color: t.neon,
  },
  name: { fontSize: 26, fontFamily: t.font.display, color: t.ink },
  tagline: { fontSize: 12, color: t.muted },
  stats: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 4 },
  stat: {
    flexBasis: 85,
    flexGrow: 1,
    gap: 4,
    backgroundColor: t.panelRaised,
    padding: 9,
    borderRadius: 7,
  },
  statLabel: {
    fontFamily: t.font.hud,
    fontSize: 9,
    letterSpacing: 0.5,
    color: t.muted,
  },
  statValue: { fontSize: 15, fontWeight: '800', color: t.amber },
  ageButton: {
    backgroundColor: t.neonDeep,
    borderRadius: 10,
    padding: 14,
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: 66,
    borderWidth: 1,
    borderColor: t.neon,
  },
  ageButtonText: {
    fontFamily: t.font.display,
    fontSize: 18,
    color: t.ink,
    fontWeight: '900',
    letterSpacing: 0.4,
  },
  ageButtonHint: { fontSize: 11, color: t.muted },
  ageIcon: { fontSize: 29, color: t.amber },
  pressed: { opacity: 0.7 },
  momentCard: {
    padding: 16,
    borderRadius: 15,
    backgroundColor: t.panelRaised,
    borderWidth: 1,
    borderColor: t.coral,
    gap: 12,
  },
  momentLabel: {
    fontFamily: t.font.hud,
    fontSize: 10,
    fontWeight: '900',
    letterSpacing: 1.2,
    color: t.neon,
  },
  momentTitle: {
    fontSize: 25,
    fontFamily: t.font.display,
    fontWeight: '700',
    color: t.ink,
  },
  momentDescription: { fontSize: 14, lineHeight: 21, color: t.ink },
  momentChoice: {
    padding: 14,
    minHeight: 52,
    borderRadius: 11,
    borderWidth: 1,
    borderColor: t.border,
    backgroundColor: t.panel,
    justifyContent: 'center',
  },
  momentChoiceText: { fontSize: 14, color: t.ink, fontWeight: '700' },
  lifeReel: {
    backgroundColor: t.panelRaised,
    borderLeftColor: t.coral,
    borderLeftWidth: 3,
    padding: 13,
    gap: 7,
    borderRadius: 5,
  },
  reelText: { color: t.ink, fontSize: 13, lineHeight: 21 },
  careerArea: {
    padding: 15,
    backgroundColor: t.panel,
    borderColor: t.border,
    borderWidth: 1,
    borderRadius: 12,
    gap: 12,
  },
  careerHeading: { flexDirection: 'row', gap: 12, alignItems: 'center' },
  careerTitle: { color: t.amber, fontFamily: t.font.display, fontSize: 20 },
  muted: { color: t.muted, fontSize: 12, lineHeight: 18 },
  careerButton: {
    backgroundColor: t.neonDeep,
    borderColor: t.neon,
    borderWidth: 1,
    borderRadius: 9,
    paddingHorizontal: 14,
    paddingVertical: 12,
    minHeight: 44,
    justifyContent: 'center',
    alignSelf: 'flex-start',
  },
  buttonText: { color: t.ink, fontSize: 12, fontWeight: '800' },
  jobs: { gap: 7 },
  jobItem: {
    backgroundColor: t.panelRaised,
    borderWidth: 1,
    borderColor: t.border,
    borderRadius: 9,
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 15,
  },
  jobTitle: { color: t.amber, fontSize: 15, fontWeight: '800' },
  actionMark: { color: t.neon, fontSize: 10, fontWeight: '900' },
  careerButtons: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  ghostButton: {
    padding: 12,
    minHeight: 44,
    justifyContent: 'center',
    borderRadius: 9,
    borderWidth: 1,
    borderColor: t.border,
  },
});
