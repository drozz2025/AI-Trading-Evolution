//+------------------------------------------------------------------+
//| NewsXAU_V1_GITHUB_TEST.mq5                                      |
//| Based on NewsXAU_V1_TEST_OTHER_NEWS.mq5                         |
//| Demo-only controlled news feed from GitHub events.json          |
//+------------------------------------------------------------------+
#property strict
#property version "1.10"
#property description "XAUUSD news EA with live MT5 calendar/BLS validation and optional GitHub-controlled demo test feed."

// This file is the GitHub-test variant. It preserves the original strategy
// and adds a multi-event demo feed read from the repository's events.json.

