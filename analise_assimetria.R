# =============================================================================
# ANÁLISE DE ÍNDICE DE ASSIMETRIA MANUAL (AI)
# AI = (RH - LH) / (RH + LH) * 100
# Welch ANOVA entre grupos: NS vs LS vs RS
# =============================================================================

setwd("C:/Users/lemeu/hands_stroke")

# --- 1. Pacotes --------------------------------------------------------------

library(readxl)
library(tidyverse)
library(knitr)
library(rstatix)
library(ggplot2)

# --- 2. Leitura e preparo dos dados -----------------------------------------

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

# --- 3. Calcular índice de assimetria ----------------------------------------


df_ai <- df %>%
  group_by(sub, lesion, variable, hand) %>%
  summarise(
    value = mean(value, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  group_by(sub, lesion, variable) %>%
  summarise(
    LH = value[hand == "LH"],
    RH = value[hand == "RH"],
    .groups = "drop"
  ) %>%
  filter(!is.na(LH), !is.na(RH), (RH + LH) != 0) %>%
  mutate(
    AI= case_when(
      lesion == "NS" ~ (RH - LH)/(RH + LH) * 100,
      lesion == "LS" ~ (LH - RH)/(LH + RH) * 100, 
      lesion == "RS" ~ (RH - LH)/(RH + LH) *100,
      TRUE ~ NA_real_
  )
)


# --- 4. Função principal: Welch ANOVA ----------------------------------------

analisar_AI <- function(variavel, dados_ai) {
  
  cat("\n")
  cat(strrep("=", 70), "\n")
  cat("VARIÁVEL:", variavel, "\n")
  cat(strrep("=", 70), "\n")
  
  d <- dados_ai %>%
    filter(variable == variavel) %>%
    droplevels()
  
  # Estatísticas descritivas
  
  cat("\n>> Estatísticas descritivas do AI por grupo:\n")
  
  desc <- d %>%
    group_by(lesion) %>%
    summarise(
      n = n(),
      media = mean(AI, na.rm = TRUE),
      dp = sd(AI, na.rm = TRUE),
      mediana = median(AI, na.rm = TRUE),
      min = min(AI, na.rm = TRUE),
      max = max(AI, na.rm = TRUE),
      .groups = "drop"
    )
  
  print(desc)
  
  # Teste t do grupo NS contra zero
  
  cat("\n>> Validação — grupo NS contra AI = 0:\n")
  
  ns_vals <- d %>%
    filter(lesion == "NS") %>%
    pull(AI)
  
  if (length(ns_vals) >= 2) {
    
    t_ns <- t.test(ns_vals, mu = 0)
    
    cat(sprintf(
      "t(%d) = %.3f, p = %.4f, média = %.2f%%\n",
      as.integer(t_ns$parameter),
      t_ns$statistic,
      t_ns$p.value,
      mean(ns_vals, na.rm = TRUE)
    ))
    
  } else {
    
    cat("Não há sujeitos suficientes no grupo NS para o teste t.\n")
    
  }
  
  # Welch ANOVA
  
  cat("\n>> Welch ANOVA:\n")
  
  welch <- oneway.test(
    AI ~ lesion,
    data = d,
    var.equal = FALSE
  )
  
  print(welch)
  
  # Tamanho de efeito: eta² aproximado
  
  modelo_aux <- aov(AI ~ lesion, data = d)
  anova_aux <- anova(modelo_aux)
  
  ss_grupo <- anova_aux[["Sum Sq"]][1]
  ss_total <- sum(anova_aux[["Sum Sq"]])
  eta2 <- ss_grupo / ss_total
  
  cat(sprintf("\n>> Tamanho de efeito:\n"))
  cat(sprintf("η² aproximado = %.3f\n", eta2))
  
  # Post-hoc Games-Howell
  
  cat("\n>> Post-hoc Games-Howell:\n")
  
  gh <- rstatix::games_howell_test(
    d,
    AI ~ lesion
  )
  
  print(gh)
  
  return(
    invisible(
      list(
        dados = d,
        descritivas = desc,
        welch = welch,
        eta2 = eta2,
        games_howell = gh
      )
    )
  )
}

# --- 5. Rodar para todas as variáveis ----------------------------------------

variaveis <- levels(df_ai$variable)

resultados_ai <- list()

for (v in variaveis) {
  resultados_ai[[v]] <- analisar_AI(v, df_ai)
}

# --- 6. Gráficos -------------------------------------------------------------

gerar_graficos <- function(dados_ai, variaveis, pasta = "graficos_AI") {
  
  dir.create(pasta, showWarnings = FALSE)
  
  for (v in variaveis) {
    
    d <- dados_ai %>%
      filter(variable == v)
    
    nome_seguro <- gsub("[^A-Za-z0-9_]", "_", v)
    
    p <- ggplot(d, aes(x = lesion, y = AI, fill = lesion)) +
      geom_hline(yintercept = 0, linetype = "dashed", color = "gray40") +
      geom_boxplot(alpha = 0.7, outlier.shape = NA, width = 0.5) +
      geom_jitter(width = 0.15, size = 2, alpha = 0.6) +
      scale_fill_manual(
        values = c(
          "NS" = "#4CAF50",
          "LS" = "#2196F3",
          "RS" = "#F44336"
        )
      ) +
      labs(
        
        x = "",
        y = "",
        fill = "Grupo",
        
      ) +
      theme_classic(base_size = 13) +
      theme(
        plot.title = element_text(face = "bold")
      )
    
    ggsave(
      filename = file.path(pasta, paste0(nome_seguro, ".png")),
      plot = p,
      width = 6,
      height = 5,
      dpi = 300
    )
  }
  
  cat("Gráficos salvos na pasta:", pasta, "\n")
}

gerar_graficos(df_ai, variaveis)

# --- 7. Salvar resultados em Markdown ----------------------------------------

sink_ai_md <- function(dados_ai, variaveis, arquivo_saida = "resultados_AI.md") {
  
  con <- file(arquivo_saida, open = "wt", encoding = "UTF-8")
  on.exit(close(con), add = TRUE)
  
  writeLines("# Resultados — Índice de Assimetria Manual (AI)\n", con)
  writeLines(paste("**Data:**", format(Sys.time(), "%d/%m/%Y %H:%M"), "\n"), con)
  writeLines("**Fórmula:** `AI = (RH - LH) / (RH + LH) × 100`  \n", con)
  writeLines("**Positivo** → vantagem mão direita | **Negativo** → vantagem mão esquerda  \n", con)
  writeLines("**Teste principal:** Welch ANOVA  \n", con)
  writeLines("**Post-hoc:** Games-Howell  \n", con)
  writeLines("---\n", con)
  
  for (v in variaveis) {
    
    d <- dados_ai %>%
      filter(variable == v) %>%
      droplevels()
    
    writeLines(paste0("## ", v, "\n"), con)
    
    # Descritivas
    
    desc <- d %>%
      group_by(lesion) %>%
      summarise(
        n = n(),
        media = round(mean(AI, na.rm = TRUE), 2),
        dp = round(sd(AI, na.rm = TRUE), 2),
        mediana = round(median(AI, na.rm = TRUE), 2),
        min = round(min(AI, na.rm = TRUE), 2),
        max = round(max(AI, na.rm = TRUE), 2),
        .groups = "drop"
      )
    
    writeLines("### Estatísticas descritivas\n", con)
    writeLines(knitr::kable(desc, format = "markdown"), con)
    writeLines("\n", con)
    
    # Validação NS
    
    ns_vals <- d %>%
      filter(lesion == "NS") %>%
      pull(AI)
    
   
    
    
    # Welch ANOVA
    
    welch <- oneway.test(
      AI ~ lesion,
      data = d,
      var.equal = FALSE
    )
    
    writeLines("### Welch ANOVA\n", con)
    
    writeLines(sprintf(
      "F(%.2f, %.2f) = %.3f, p = %.4f\n\n",
      welch$parameter[1],
      welch$parameter[2],
      welch$statistic,
      welch$p.value
    ), con)
    
    # Eta² aproximado
    
    modelo_aux <- aov(AI ~ lesion, data = d)
    anova_aux <- anova(modelo_aux)
    
    ss_grupo <- anova_aux[["Sum Sq"]][1]
    ss_total <- sum(anova_aux[["Sum Sq"]])
    eta2 <- ss_grupo / ss_total
    
    writeLines("### Tamanho de efeito\n", con)
    writeLines(sprintf("η² aproximado = %.3f\n\n", eta2), con)
    
    # Post-hoc Games-Howell
    
    gh <- rstatix::games_howell_test(
      d,
      AI ~ lesion
    )
    
    writeLines("### Post-hoc Games-Howell\n", con)
    writeLines(knitr::kable(as.data.frame(gh), format = "markdown", digits = 4), con)
    writeLines("\n", con)
    
    writeLines("---\n", con)
  }
  
  cat("Resultados salvos em:", arquivo_saida, "\n")
}

sink_ai_md(df_ai, variaveis)