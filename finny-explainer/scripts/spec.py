# Script + shot list. Times are source-video seconds.
# shot kinds: ("still",t) ("clip",a,b[,speed]) ("custom",name)
SECTIONS = [
 dict(id="intro", chip="Meet Finny", head=["Know when you'll be", "*financially free*"], theme="light", lines=[
  ("Do you know when you'll be financially free? Finny does.", [("custom","title"),("still",13.0)]),
  ("Finny tells you your FIRE age, and the corpus you need to get there,", [("still",15.3)]),
  ("shows how you can get there faster,", [("still",17.0)]),
  ("and gets your portfolio reviewed by an expert advisor.", [("still",19.5)]),
 ]),
 dict(id="start", chip="01  ·  Get started", head=["Your FIRE report", "in *3 minutes*"], theme="light", lines=[
  ("Sign in with your phone number and OTP, and see your map to a FIRE report, in just three minutes.", [("clip",22.0,24.6),("clip",26.0,29.0),("clip",31.0,33.6)]),
  ("Enter your PAN. Finny verifies it, and fetches the name linked to it.", [("clip",35.0,37.4),("clip",49.0,57.4,2.0),("clip",58.0,61.0)]),
 ]),
 dict(id="aa", chip="02  ·  Account Aggregator", head=["Discover & link", "*every account*"], theme="light", lines=[
  ("Next, using the Account Aggregator framework, Finny discovers the accounts linked to your phone and PAN.", [("clip",67.0,71.5),("clip",73.0,77.5),("clip",91.0,107.0,3.0)]),
  ("Banks, mutual funds, stocks and NPS, all in one place.", [("still",122.6)]),
  ("Give your consent once, and every account is securely fetched and linked.", [("clip",159.4,163.6),("clip",169.0,172.6)]),
 ]),
 dict(id="mf", chip="03  ·  MF Central", head=["Mutual funds,", "*securely fetched*"], theme="light", lines=[
  ("Your mutual fund transactions come in through M F Central, over a secure connection.", [("clip",174.2,176.6),("clip",177.2,179.6),("clip",181.0,183.0),("clip",187.0,189.2),("clip",190.6,193.0)]),
  ("Then choose who you're planning for: just yourself, or your family.", [("clip",197.2,199.0),("clip",200.0,206.0)]),
 ]),
 dict(id="orbit", chip="04  ·  Fetching", head=["All your data,", "*in real time*"], theme="light", lines=[
  ("Finny pulls everything together, in real time.", [("clip",214.0,217.2),("clip",268.4,270.2)]),
 ]),
 dict(id="assets", chip="05  ·  Review assets", head=["Assets, additions", "& *inheritance*"], theme="light", lines=[
  ("Review the assets fetched automatically,", [("clip",274.2,278.0)]),
  ("add anything we couldn't fetch, like gold, real estate or P F,", [("clip",280.0,282.0),("clip",284.0,286.6),("clip",299.0,301.0)]),
  ("and any inheritance you expect, with its value, and when it might arrive.", [("clip",303.6,306.0),("clip",311.0,314.6),("clip",316.0,318.6)]),
 ]),
 dict(id="cash", chip="06  ·  Income & spends", head=["Cash flow,", "*auto-categorised*"], theme="light", lines=[
  ("Your income and spends are auto-fetched from your bank accounts, and categorised into salary, dividends and interest.", [("clip",322.0,323.0),("clip",324.0,327.0),("clip",329.0,334.4)]),
  ("Looks good.", [("clip",388.0,389.6)]),
 ]),
 dict(id="check", chip="07  ·  One last check", head=["Net worth, cash flow", "& *assumptions*"], theme="light", lines=[
  ("One final check of your net worth, cash flow and assumptions,", [("clip",390.0,402.0,2.0)]),
  ("and Finny's proprietary models calculate your FIRE age.", [("clip",422.0,429.0),("clip",442.4,446.0)]),
 ]),
 dict(id="age", chip="08  ·  Your FIRE age", head=["Two ages.", "*One plan.*"], theme="dark", lines=[
  ("Based on your lifestyle, you get two FIRE ages. Fifty two, at your current pace,", [("custom","age1")]),
  ("and forty three, with the right plan from Finny. That's nine years sooner.", [("custom","age2")]),
 ]),
 dict(id="report", chip="09  ·  FIRE report", head=["Your FIRE", "*score*"], theme="light", lines=[
  ("Your FIRE score shows where your portfolio is doing well, and where it needs attention,", [("custom","rep0")]),
  ("across foundations, like your savings rate,", [("custom","rep1")]),
  ("investment momentum,", [("custom","rep2")]),
  ("and risk and resilience, like your exposure to low-growth assets.", [("custom","rep3")]),
 ]),
 dict(id="call", chip="10  ·  Expert review", head=["A free call with an", "*expert advisor*"], theme="light", lines=[
  ("When you're ready, book a free portfolio review with an expert advisor.", [("clip",621.0,627.6)]),
  ("Pick a time that suits you, and the invite lands in your inbox.", [("clip",630.4,632.6),("clip",643.0,645.4),("clip",638.3,639.4),("clip",646.0,648.2)]),
 ]),
 dict(id="outro", chip="", head=[], theme="dark", lines=[
  ("From there, you can continue as a paid advisory client.", [("custom","out1")]),
  ("Finny's financial models create your plan, expert advisors walk you through it, and AI agents execute it.", [("custom","out2")]),
  ("That's how Finny becomes your one-stop shop for financial independence.", [("custom","end")]),
 ]),
]
