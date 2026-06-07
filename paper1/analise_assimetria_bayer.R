# =============================================================================
# ANÁLISE BAYESIANA DO ÍNDICE DE ASSIMETRIA MANUAL (AI)
# AI clínico por grupo
# Bayes Factor para comparação entre grupos
# =============================================================================

setwd("C:/Users/lemeu/hands_stroke")

# --- 1. Pacotes --------------------------------------------------------------

# install.packages("readxl")
# install.packages("tidyverse")
# install.packages("BayesFactor")
# install.packages("knitr")

library(readxl)
library(tidyverse)
library(BayesFactor)
library(knitr)

# --- 2. Leitura dos dados ----------------------------------------------------

arquivo <- "data.xlsx"
abas <- excel_sheets(arquivo)

df <- map_dfr(abas, function(aba) {
  
  d <- read_excel(arquivo, sheet = aba)
  
  d <- d[, c("sub", "lesion", "hand", "valor")]
  
  names(d)[names(d) == "valor"] <- "value"
  
  d$variable <- aba
  
  d
})

df <- df %>%
  mutate(
    sub = factor(sub),
    lesion = factor(lesion, levels = c("NS", "LS", "RS")),
    hand = factor(hand, levels = c("LH", "RH")),
    variable = factor(variable)
  )

# --- 3. Calcular AI ----------------------------------------------------------

df_ai <- df %>%
  group_by(sub, lesion, variable, hand) %>%
  summarise(
    value = mean(value, na.rm = TRUE),
    n_valid = sum(!is.na(value)),
    .groups = "drop"
  ) %>%
  filter(n_valid > 0) %>%
  group_by(sub, lesion, variable) %>%
  summarise(
    LH = first(value[hand == "LH"]),
    RH = first(value[hand == "RH"]),
    n_LH = first(n_valid[hand == "LH"]),
    n_RH = first(n_valid[hand == "RH"]),
    .groups = "drop"
  ) %>%
  filter(
    !is.na(LH),
    !is.na(RH),
    (LH + RH) != 0
  ) %>%
  mutate(
    AI = case_when(
      lesion == "NS" ~ (RH - LH) / (RH + LH) * 100,
      lesion == "LS" ~ (LH - RH) / (LH + RH) * 100,
      lesion == "RS" ~ (RH - LH) / (RH + LH) * 100,
      TRUE ~ NA_real_
    )
  )

# --- 4. Função para ANOVA Bayesiana ------------------------------------------

analisar_bayes_AI <- function(variavel, dados_ai) {
  
  cat("\n")
  cat(strrep("=", 70), "\n")
  cat("VARIÁVEL:", variavel, "\n")
  cat(strrep("=", 70), "\n")
  
  d <- dados_ai %>%
    filter(variable == variavel) %>%
    droplevels()
  
  # Descritivas
  
  desc <- d %>%
    group_by(lesion) %>%
    summarise(
      n = n(),
      media = mean(AI, na.rm = TRUE),
      dp = sd(AI, na.rm = TRUE),
      mediana = median(AI, na.rm = TRUE),
      .groups = "drop"
    )
  
  cat("\n>> Estatísticas descritivas:\n")
  print(desc)
  
  # ANOVA Bayesiana
  
  cat("\n>> ANOVA Bayesiana:\n")
  
  bf_modelo <- anovaBF(
    AI ~ lesion,
    data = d
  )
  
  print(bf_modelo)
  
  bf10 <- extractBF(bf_modelo)$bf
  bf01 <- 1 / bf10
  
  cat(sprintf("\nBF10 = %.3f\n", bf10))
  cat(sprintf("BF01 = %.3f\n", bf01))
  
  # Interpretação simples
  
  cat("\nInterpretação:\n")
  
  if (bf10 < 1/3) {
    cat("Evidência a favor da hipótese nula.\n")
  } else if (bf10 < 1) {
    cat("Evidência fraca a favor da hipótese nula.\n")
  } else if (bf10 < 3) {
    cat("Evidência anedótica/fraca a favor de diferença entre grupos.\n")
  } else if (bf10 < 10) {
    cat("Evidência moderada a favor de diferença entre grupos.\n")
  } else if (bf10 < 30) {
    cat("Evidência forte a favor de diferença entre grupos.\n")
  } else {
    cat("Evidência muito forte a favor de diferença entre grupos.\n")
  }
  
  # Comparações bayesianas par-a-par
  
  cat("\n>> Comparações par-a-par Bayesianas:\n")
  
  pares <- combn(levels(d$lesion), 2, simplify = FALSE)
  
  posthoc <- map_dfr(pares, function(par) {
    
    d_par <- d %>%
      filter(lesion %in% par) %>%
      droplevels()
    
    bf_t <- ttestBF(
      formula = AI ~ lesion,
      data = d_par
    )
    
    bf10_par <- extractBF(bf_t)$bf
    
    tibble(
      comparacao = paste(par[1], "vs", par[2]),
      BF10 = bf10_par,
      BF01 = 1 / bf10_par
    )
  })
  
  print(posthoc)
  
  return(
    invisible(
      list(
        dados = d,
        descritivas = desc,
        bayes_anova = bf_modelo,
        BF10 = bf10,
        BF01 = bf01,
        posthoc = posthoc
      )
    )
  )
}

# --- 5. Rodar para todas as variáveis ----------------------------------------

variaveis <- levels(df_ai$variable)

resultados_bayes <- list()

for (v in variaveis) {
  resultados_bayes[[v]] <- analisar_bayes_AI(v, df_ai)
}

# --- 6. Salvar resultados em Markdown ----------------------------------------

salvar_bayes_md <- function(resultados_bayes,
                            arquivo_saida = "resultados_AI_bayesiano.md") {
  
  con <- file(arquivo_saida, open = "wt", encoding = "UTF-8")
  on.exit(close(con), add = TRUE)
  
  writeLines("# Resultados Bayesianos — Índice de Assimetria Manual\n", con)
  writeLines(paste("**Data:**", format(Sys.time(), "%d/%m/%Y %H:%M"), "\n"), con)
  writeLines("**Análise principal:** ANOVA Bayesiana  \n", con)
  writeLines("**Post-hoc:** testes t bayesianos par-a-par  \n", con)
  writeLines("---\n", con)
  
  for (v in names(resultados_bayes)) {
    
    res <- resultados_bayes[[v]]
    
    writeLines(paste0("## ", v, "\n"), con)
    
    writeLines("### Estatísticas descritivas\n", con)
    writeLines(
      knitr::kable(
        res$descritivas,
        format = "markdown",
        digits = 3
      ),
      con
    )
    writeLines("\n", con)
    
    writeLines("### ANOVA Bayesiana\n", con)
    
    writeLines(sprintf(
      "BF10 = %.3f  \nBF01 = %.3f\n\n",
      res$BF10,
      res$BF01
    ), con)
    
    writeLines("### Comparações par-a-par Bayesianas\n", con)
    
    writeLines(
      knitr::kable(
        res$posthoc,
        format = "markdown",
        digits = 3
      ),
      con
    )
    
    writeLines("\n---\n", con)
  }
  
  cat("Resultados bayesianos salvos em:", arquivo_saida, "\n")
}

salvar_bayes_md(resultados_bayes)
