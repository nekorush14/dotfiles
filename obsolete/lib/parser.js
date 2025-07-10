module.exports = {
  onWillParseMarkdown: function (markdown) {
    return new Promise((resolve, reject) => {
      return resolve(markdown)
    })
  },
  onDidParseMarkdown: function (html, { cheerio }) {
    return new Promise((resolve, reject) => {
      return resolve(html)
    })
  },
  onWillTransformMarkdown: function (markdown) {
    return new Promise((resolve, reject) => {
      return resolve(markdown);
    });
  },
  onDidTransformMarkdown: function (markdown) {
    return new Promise((resolve, reject) => {
      return resolve(markdown);
    });
  }
}

const useHTMLBadges = true;
// const notificationTypes = {
//   NOTE: {
//     header: "Note",
//     md_icon: ":hand:",
//     html_icon: "✋",
//     background: "#9577c9",
//     color: "#fff1cc",
//   },
//   TIP: {
//     header: "Tip",
//     md_icon: ":bulb:",
//     html_icon: "💡",
//     background: "#d2f9d2",
//     color: "#094409",
//   },
//   INFO: {
//     header: "Information",
//     md_icon: ":heavy_exclamation_mark:",
//     html_icon: "❗",
//     background: "#e0f2ff",
//     color: "#002b4d",
//   },
//   WARNING: {
//     header: "Warning",
//     md_icon: ":warning:",
//     html_icon: "⚠",
//     background: "#fff1cc",
//     color: "#664b00",
//   },
//   CAUTION: {
//     header: "Be careful!",
//     md_icon: ":no_entry_sign:",
//     html_icon: "🚫",
//     background: "#ffdacc",
//     color: "#651b01",
//   },
// };
const notificationTypes = {
  NOTE: {
    header: 'Note',
    md_icon: ':hand:',
    html_icon: '✋',
    color: 'black',
    background: '#9374c9',
    body_color: 'black',
  },
  TIP: {
    header: 'Tip',
    md_icon: ':bulb:',
    html_icon: '💡',
    color: 'black',
    background: '#65c565',
    body_color: 'black',
  },
  INFO: {
    header: 'Information',
    md_icon: ':heavy_exclamation_mark:',
    html_icon: 'ℹ️',
    color: 'black',
    background: '#4ba1e2',
    body_color: 'black',
  },
  WARNING: {
    header: 'Warning',
    md_icon: ':warning:',
    html_icon: '⚠️',
    color: 'black',
    background: '#e0e26a',
    body_color: 'black',
  },
  CAUTION: {
    header: 'Caution',
    md_icon: ':no_entry_sign:',
    html_icon: '🚫',
    color: 'black',
    background: '#cf6679',
    body_color: 'black',
  },
};
// HELPERS
const errorParser = (err) => `<pre>${err.stack}</pre>`;

const markdownParse = (markdown) => {
  // [!NOTE] Example Text
  let notificationRegex = null;

  for ([notificationType, notificationInfo] of Object.entries(
    notificationTypes,
  )) {
    // multi line comments
    notificationRegex = new RegExp(
      String.raw`\[\!${notificationType}\](.+\r?\n?)+(?=(\r?\n)?)`,
      'gm',
    );

    markdown = markdown.replace(notificationRegex, (message) => {
      return `> ${notificationInfo.md_icon} **${notificationInfo.header}**
                ${message.substr(message.indexOf(' ') + 1)}`;
    });
  }

  return markdown;
};

const htmlParse = (html) => {
  const findCitations = (html) =>
    html.match(/<blockquote>[\S\s]*?<\/blockquote>/gi);

  const findBadges = (citationArray) => {
    let realBadges = [];

    for (index in citationArray) {
      for ([_, info] of Object.entries(notificationTypes)) {
        // minified version spits out <br> instead of <br />
        if (
          citationArray[index].match(
            `<strong>${info.header}<\/strong><br>`,
            'gm',
          )
        ) {
          realBadges[index] = citationArray[index];
        }
      }
    }

    return realBadges;
  };

  let badges = findCitations(html);
  badges = findBadges(badges);

  const getBadgeInfos = (badgeElement) => {
    let findTitle = '';

    for ([_, info] of Object.entries(notificationTypes)) {
      // returns a array of matches
      // minified version spits out <br> instead of <br />
      findTitle = badgeElement.match(
        `.*<strong>${info.header}<\/strong><br>`,
        'gm',
      );
      if (findTitle != null) {
        if (findTitle.length != 0) return info;
      }
    }

    return {};
  };

  const getBody = (badgeElement) => {
    // minified version spits out <br> instead of <br />
    const findBody = badgeElement.match(`(?<=<br>)(.|\r?\n)*?(?=<\/p>)`);

    if (findBody != null) {
      if (findBody.length != 0) return findBody[0].trim();
    }

    return '';
  };

  let infos = {};
  let body = '';

  for (index in badges) {
    html = html.replace(badges[index], (foundElement) => {
      infos = getBadgeInfos(foundElement);
      body = getBody(foundElement);

      if (infos == null)
        return `<div style="color:black">parsing error, see: <pre>~/.mume/parser.js</pre></div>`;

      const styling = `style="padding: 0.8rem 1rem; border-radius: 6px; margin: 1rem 0; background-color:${info.background}"`;

      return `<div ${styling}><p>${info.html_icon} <strong style="color: ${info.color}">${info.header}</strong></p><p style="margin: 0; text-align: left; line-height:1.3; color: ${info.body_color}">${body}</p></div>`;
    });
  }

  return html;
};

module.exports = {
  // do something with the markdown before it gets parsed to HTML
  onWillParseMarkdown: function (markdown) {
    return new Promise((resolve, reject) => {
      try {
        markdown = markdownParse(markdown);
      } catch (error) {
        markdown = errorParser(error);
      }

      return resolve(markdown);
    });
  },
  // do something with the parsed HTML string
  onDidParseMarkdown: function (html) {
    return new Promise((resolve, reject) => {
      try {
        html = useHTMLBadges ? htmlParse(html) : html;
      } catch (error) {
        html = errorParser(error);
      }

      return resolve(html);
    });
  },
};