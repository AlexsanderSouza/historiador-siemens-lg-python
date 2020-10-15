import _ from 'lodash';
import moment from 'moment';

import { RawTimeRange } from '@grafana/ui';

import * as dateMath from './datemath';

const spans = {
  s: { display: 'segundo' },
  m: { display: 'minuto' },
  h: { display: 'hora' },
  d: { display: 'dia' },
  w: { display: 'semana' },
  M: { display: 'mês' },
  y: { display: 'ano' },
};

const rangeOptions = [
  { from: 'now/d', to: 'now/d', display: 'Hoje', section: 2 },
  { from: 'now/d', to: 'now', display: 'Hoje até agora', section: 2 },
  { from: 'now/w', to: 'now/w', display: 'Essa semana', section: 2 },
  { from: 'now/w', to: 'now', display: 'Essa semana até agora', section: 2 },
  { from: 'now/M', to: 'now/M', display: 'Esse mês', section: 2 },
  { from: 'now/M', to: 'now', display: 'Esse Mês até agora', section: 2 },
  { from: 'now/y', to: 'now/y', display: 'Esse ano', section: 2 },
  { from: 'now/y', to: 'now', display: 'Esse ano até agora', section: 2 },

  { from: 'now-1d/d', to: 'now-1d/d', display: 'Ontem', section: 1 },
  {
    from: 'now-2d/d',
    to: 'now-2d/d',
    display: 'Anteontem',
    section: 1,
  },
  {
    from: 'now-7d/d',
    to: 'now-7d/d',
    display: 'Uma semana atrás',
    section: 1,
  },
  { from: 'now-1w/w', to: 'now-1w/w', display: 'Semana passada', section: 1 },
  { from: 'now-1M/M', to: 'now-1M/M', display: 'Mês passado', section: 1 },
  { from: 'now-1y/y', to: 'now-1y/y', display: 'Ano passado', section: 1 },

  { from: 'now-5m', to: 'now', display: 'Ultimos 5 Minutos', section: 3 },
  { from: 'now-15m', to: 'now', display: 'Ultimos 15 Minutos', section: 3 },
  { from: 'now-30m', to: 'now', display: 'Ultimos 30 Minutos', section: 3 },
  { from: 'now-1h', to: 'now', display: 'Ultima 1 hora', section: 3 },
  { from: 'now-3h', to: 'now', display: 'Ultimas 3 horas', section: 3 },
  { from: 'now-6h', to: 'now', display: 'Ultimas 6 horas', section: 3 },
  { from: 'now-12h', to: 'now', display: 'Ultimas 12 horas', section: 3 },
  { from: 'now-24h', to: 'now', display: 'Ultimas 24 horas', section: 3 },

  { from: 'now-2d', to: 'now', display: 'Ultimos 2 dias', section: 0 },
  { from: 'now-7d', to: 'now', display: 'Ultimos 7 dias', section: 0 },
  { from: 'now-30d', to: 'now', display: 'Ultimos 30 dias', section: 0 },
  { from: 'now-90d', to: 'now', display: 'Ultimos 90 dias', section: 0 },
  { from: 'now-6M', to: 'now', display: 'Ultimos 6 mesês', section: 0 },
  { from: 'now-1y', to: 'now', display: 'Ultimo 1 ano', section: 0 },
  { from: 'now-2y', to: 'now', display: 'Ultimos 2 anos', section: 0 },
  { from: 'now-5y', to: 'now', display: 'Ultimos 5 anos', section: 0 },
];

const absoluteFormat = 'MMM D, YYYY HH:mm:ss';

const rangeIndex = {};
_.each(rangeOptions, frame => {
  rangeIndex[frame.from + ' to ' + frame.to] = frame;
});

export function getRelativeTimesList(timepickerSettings, currentDisplay) {
  const groups = _.groupBy(rangeOptions, (option: any) => {
    option.active = option.display === currentDisplay;
    return option.section;
  });

  // _.each(timepickerSettings.time_options, (duration: string) => {
  //   let info = describeTextRange(duration);
  //   if (info.section) {
  //     groups[info.section].push(info);
  //   }
  // });

  return groups;
}

function formatDate(date) {
  return date.format(absoluteFormat);
}

// handles expressions like
// 5m
// 5m to now/d
// now/d to now
// now/d
// if no to <expr> then to now is assumed
export function describeTextRange(expr: any) {
  const isLast = expr.indexOf('+') !== 0;
  if (expr.indexOf('now') === -1) {
    expr = (isLast ? 'now-' : 'now') + expr;
  }

  let opt = rangeIndex[expr + ' to now'];
  if (opt) {
    return opt;
  }

  if (isLast) {
    opt = { from: expr, to: 'now' };
  } else {
    opt = { from: 'now', to: expr };
  }

  const parts = /^now([-+])(\d+)(\w)/.exec(expr);
  if (parts) {
    const unit = parts[3];
    const amount = parseInt(parts[2], 10);
    const span = spans[unit];
    if (span) {
      opt.display = isLast ? 'Last ' : 'Next ';
      opt.display += amount + ' ' + span.display;
      opt.section = span.section;
      if (amount > 1) {
        opt.display += 's';
      }
    }
  } else {
    opt.display = opt.from + ' to ' + opt.to;
    opt.invalid = true;
  }

  return opt;
}

export function describeTimeRange(range: RawTimeRange): string {
  const option = rangeIndex[range.from.toString() + ' to ' + range.to.toString()];
  if (option) {
    return option.display;
  }

  if (moment.isMoment(range.from) && moment.isMoment(range.to)) {
    return formatDate(range.from) + ' to ' + formatDate(range.to);
  }

  if (moment.isMoment(range.from)) {
    const toMoment = dateMath.parse(range.to, true);
    return formatDate(range.from) + ' to ' + toMoment.fromNow();
  }

  if (moment.isMoment(range.to)) {
    const from = dateMath.parse(range.from, false);
    return from.fromNow() + ' to ' + formatDate(range.to);
  }

  if (range.to.toString() === 'now') {
    const res = describeTextRange(range.from);
    return res.display;
  }

  return range.from.toString() + ' to ' + range.to.toString();
}

export const isValidTimeSpan = (value: string) => {
  if (value.indexOf('$') === 0 || value.indexOf('+$') === 0) {
    return true;
  }

  const info = describeTextRange(value);
  return info.invalid !== true;
};
