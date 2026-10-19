// Builds the editable A4 Word book (Kilkari_Hindi_Class2.docx) from content.js and images/.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, BorderStyle, PageBreak, Header, Footer, PageNumber, LevelFormat, VerticalAlign,
  PageBorderDisplay, PageBorderOffsetFrom, TableLayoutType, LineRuleType,
} = require("docx");
const book = require("./content");

const FONT = { ascii: "Nirmala UI", hAnsi: "Nirmala UI", cs: "Nirmala UI", eastAsia: "Nirmala UI" };
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1000; // A4 in DXA, ~1.76 cm margins
const CONTENT_W = PAGE_W - 2 * MARGIN;
const BODY_SIZE = 32; // half-points → 16 pt body text for Class 2 readers

const img = (name, width = 500) => {
  const h = Math.round(width * 330 / 600);
  return new ImageRun({
    type: "png",
    data: fs.readFileSync(path.join(__dirname, "images", name + ".png")),
    transformation: { width, height: h },
    altText: { title: name, description: name, name },
  });
};

const run = (text, o = {}) => new TextRun({
  text, font: FONT, size: o.size || BODY_SIZE, sizeComplexScript: o.size || BODY_SIZE,
  bold: o.bold, boldComplexScript: o.bold, color: o.color, italics: o.italics,
});

const para = (children, o = {}) => new Paragraph({
  children: Array.isArray(children) ? children : [children],
  alignment: o.align || AlignmentType.LEFT,
  spacing: { before: o.before || 0, after: o.after ?? 100, line: o.line || 336, lineRule: LineRuleType.AUTO },
  indent: o.indent,
  shading: o.shade ? { type: ShadingType.CLEAR, color: "auto", fill: o.shade } : undefined,
  border: o.border,
  keepNext: o.keepNext,
});

const cell = (children, o = {}) => new TableCell({
  children,
  width: { size: o.width, type: WidthType.DXA },
  shading: o.fill ? { type: ShadingType.CLEAR, color: "auto", fill: o.fill } : undefined,
  verticalAlign: VerticalAlign.CENTER,
  margins: { top: o.pad ?? 80, bottom: o.pad ?? 80, left: 140, right: 140 },
  borders: o.borders,
});

const noBorders = {
  top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
};

// light tint of a chapter colour for boxes and table rows
const tint = (hex, amt) => {
  const n = parseInt(hex, 16);
  const ch = (s) => Math.round(((n >> s) & 255) + (255 - ((n >> s) & 255)) * amt);
  return [16, 8, 0].map((s) => ch(s).toString(16).padStart(2, "0")).join("").toUpperCase();
};

const banner = (label, title, color) => new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: [2000, CONTENT_W - 2000],
  layout: TableLayoutType.FIXED,
  rows: [new TableRow({
    children: [
      cell([para(run(label, { size: 26, bold: true, color: color }), { align: AlignmentType.CENTER, after: 0 })],
        { width: 2000, fill: "FFF59D", borders: noBorders }),
      cell([para(run(title, { size: 44, bold: true, color: "FFFFFF" }), { align: AlignmentType.CENTER, after: 0 })],
        { width: CONTENT_W - 2000, fill: color, borders: noBorders }),
    ],
  })],
});

const picture = (name, caption, color, width) => [
  para(img(name, width), { align: AlignmentType.CENTER, before: 120, after: 20, keepNext: true }),
  para(run(caption, { size: 22, italics: true, color }), { align: AlignmentType.CENTER, after: 120 }),
];

const sectionHeading = (text, color) => para(run(text, { size: 28, bold: true, color: "FFFFFF" }),
  { shade: color, before: 140, after: 100, line: 276, indent: { left: 0 } });

function exercisePage(ch, idx) {
  const c = ch.color;
  const out = [
    para(run("अभ्यास", { size: 44, bold: true, color: c }), { align: AlignmentType.CENTER, after: 40 }),
    para(run(`पाठ ${idx + 1} — ${ch.title}`, { size: 26, color: "555555" }), {
      align: AlignmentType.CENTER, after: 160,
      border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: c, space: 4 } },
    }),
    sectionHeading("  (क) शब्द-अर्थ", c),
  ];
  const w1 = 3300, w2 = CONTENT_W - w1;
  out.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [w1, w2],
    rows: [
      new TableRow({
        tableHeader: true,
        children: [
          cell([para(run("शब्द", { bold: true, color: "FFFFFF" }), { align: AlignmentType.CENTER, after: 0 })], { width: w1, fill: tint(c, 0.15) }),
          cell([para(run("अर्थ", { bold: true, color: "FFFFFF" }), { align: AlignmentType.CENTER, after: 0 })], { width: w2, fill: tint(c, 0.15) }),
        ],
      }),
      ...ch.words.map(([w, m], i) => new TableRow({
        children: [
          cell([para(run(w, { bold: true, color: c, size: 28 }), { align: AlignmentType.CENTER, after: 0, line: 276 })], { width: w1, pad: 40, fill: i % 2 ? "FFFFFF" : tint(c, 0.88) }),
          cell([para(run(m, { size: 28 }), { after: 0, line: 276 })], { width: w2, pad: 40, fill: i % 2 ? "FFFFFF" : tint(c, 0.88) }),
        ],
      })),
    ],
  }));

  out.push(sectionHeading("  (ख) प्रश्न-उत्तर — इन प्रश्नों के उत्तर लिखो", c));
  ch.questions.forEach((q) => out.push(new Paragraph({
    children: [run(q, { size: 28 })],
    numbering: { reference: `q${idx}`, level: 0 },
    spacing: { after: 100, line: 300, lineRule: LineRuleType.AUTO },
  })));

  out.push(sectionHeading("  (ग) कठिन शब्द — इन्हें पढ़ो और लिखो", c));
  const cols = 5, cw = Math.floor(CONTENT_W / cols);
  const palette = ["FFCDD2", "FFE0B2", "FFF9C4", "C8E6C9", "BBDEFB", "E1BEE7"];
  const rows = [];
  for (let r = 0; r < Math.ceil(ch.spellings.length / cols); r++) {
    rows.push(new TableRow({
      children: Array.from({ length: cols }, (_, k) => {
        const word = ch.spellings[r * cols + k] || "";
        return cell([para(run(word, { bold: true, size: 28, color: "263238" }), { align: AlignmentType.CENTER, after: 0 })],
          { width: cw, pad: 60, fill: palette[(r * cols + k) % palette.length] });
      }),
    }));
  }
  out.push(new Table({ width: { size: cw * cols, type: WidthType.DXA }, columnWidths: Array(cols).fill(cw), rows }));
  return out;
}

function storyBody(ch) {
  const out = [];
  ch.body.forEach((b) => {
    if (typeof b === "string") {
      out.push(para(run(b), { indent: { firstLine: 500 }, after: 90, align: AlignmentType.JUSTIFIED }));
    } else {
      out.push(...picture(b.img, b.caption, ch.color, 470));
    }
  });
  out.push(para([run("सीख: ", { bold: true, color: ch.color }), run(ch.moral, { bold: true })], {
    shade: tint(ch.color, 0.85), before: 120, after: 0, align: AlignmentType.CENTER,
    border: { left: { style: BorderStyle.SINGLE, size: 24, color: ch.color, space: 6 } },
  }));
  return out;
}

function poemBody(ch) {
  const out = [...picture(ch.img, ch.caption, ch.color, 420)];
  ch.stanzas.forEach((st, si) => {
    st.forEach((line, li) => out.push(para(run(line, { size: 30, bold: true, color: si % 2 ? "37474F" : ch.color }), {
      align: AlignmentType.CENTER, after: li === st.length - 1 ? 200 : 0, line: 300,
    })));
  });
  return out;
}

const pageBorder = (color) => ({
  pageBorders: { display: PageBorderDisplay.ALL_PAGES, offsetFrom: PageBorderOffsetFrom.PAGE },
  pageBorderTop: { style: BorderStyle.DOUBLE, size: 18, color, space: 24 },
  pageBorderBottom: { style: BorderStyle.DOUBLE, size: 18, color, space: 24 },
  pageBorderLeft: { style: BorderStyle.DOUBLE, size: 18, color, space: 24 },
  pageBorderRight: { style: BorderStyle.DOUBLE, size: 18, color, space: 24 },
});

const pageProps = (color) => ({
  page: {
    size: { width: PAGE_W, height: PAGE_H },
    margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN, header: 450, footer: 450 },
    borders: pageBorder(color),
  },
});

const header = (text, color) => new Header({
  children: [para(run(text, { size: 20, color }), { align: AlignmentType.RIGHT, after: 0 })],
});
const footer = (color) => new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 22, bold: true, color })],
  })],
});

// ---------------------------------------------------------------- cover + contents
const cover = [
  para([], { after: 300 }),
  para(run(book.bookTitle, { size: 120, bold: true, color: "E65100" }), { align: AlignmentType.CENTER, after: 0, line: 240 }),
  para(run(book.bookSubtitle, { size: 40, bold: true, color: "1565C0" }), { align: AlignmentType.CENTER, after: 300 }),
  para(img("cover", 600), { align: AlignmentType.CENTER, after: 300 }),
  para(run("5 रोचक कहानियाँ  •  2 मधुर कविताएँ  •  रंग-बिरंगे चित्र", { size: 30, bold: true, color: "6A1B9A" }),
    { align: AlignmentType.CENTER, after: 500 }),
  ...["नाम : ______________________________", "कक्षा : ________     अनुभाग : ________", "विद्यालय : ___________________________"]
    .map((t) => para(run(t, { size: 32, color: "37474F" }), { align: AlignmentType.CENTER, after: 200 })),
];

const tw = [1400, CONTENT_W - 1400 - 2200, 2200];
const contents = [
  para(run("विषय-सूची", { size: 52, bold: true, color: "C62828" }), { align: AlignmentType.CENTER, after: 300 }),
  new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: tw,
    rows: [
      new TableRow({
        tableHeader: true,
        children: ["क्रम", "पाठ का नाम", "विधा"].map((h, i) =>
          cell([para(run(h, { bold: true, color: "FFFFFF", size: 32 }), { align: AlignmentType.CENTER, after: 0 })], { width: tw[i], fill: "C62828" })),
      }),
      ...book.chapters.map((ch, i) => new TableRow({
        children: [
          cell([para(run(`${i + 1}.`, { bold: true, size: 32, color: ch.color }), { align: AlignmentType.CENTER, after: 0 })], { width: tw[0], fill: tint(ch.color, 0.88) }),
          cell([para(run(ch.title, { bold: true, size: 32, color: ch.color }), { after: 0 })], { width: tw[1], fill: tint(ch.color, 0.88) }),
          cell([para(run(ch.type === "story" ? "कहानी" : "कविता", { size: 30 }), { align: AlignmentType.CENTER, after: 0 })], { width: tw[2], fill: tint(ch.color, 0.88) }),
        ],
      })),
    ],
  }),
  para([], { after: 300 }),
  para(run("हर पाठ के बाद अभ्यास में दिए गए हैं —", { size: 30, bold: true, color: "37474F" }), { before: 300, after: 120 }),
  ...["शब्द-अर्थ", "प्रश्न-उत्तर", "कठिन शब्द"].map((t, i) => new Paragraph({
    children: [run(t, { size: 30 })], numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 },
  })),
];

// ---------------------------------------------------------------- assemble
const numbering = {
  config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "★", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } }, run: { color: "E65100" } } }] },
    ...book.chapters.map((_, i) => ({
      reference: `q${i}`,
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 600, hanging: 450 } }, run: { bold: true, font: FONT } } }],
    })),
  ],
};

const sections = [
  { properties: pageProps("FF8A00"), children: [...cover, new Paragraph({ children: [new PageBreak()] }), ...contents] },
  ...book.chapters.map((ch, i) => ({
    properties: pageProps(ch.color),
    headers: { default: header(`${book.bookTitle} — ${book.bookSubtitle}  |  पाठ ${i + 1}: ${ch.title}`, ch.color) },
    footers: { default: footer(ch.color) },
    children: [
      banner(`पाठ ${i + 1}` + (ch.type === "story" ? " • कहानी" : " • कविता"), ch.title, ch.color),
      ...(ch.type === "story" ? storyBody(ch) : poemBody(ch)),
      new Paragraph({ children: [new PageBreak()] }),
      ...exercisePage(ch, i),
    ],
  })),
];

const doc = new Document({
  creator: "Kilkari",
  title: `${book.bookTitle} — ${book.bookSubtitle}`,
  styles: { default: { document: { run: { font: FONT, size: BODY_SIZE } } } },
  numbering,
  sections,
});

const out = process.argv[2] || path.join(__dirname, "Kilkari_Hindi_Class2.docx");
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(out, buf); console.log("wrote", out); });
