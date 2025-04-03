import java.time.LocalDateTime;
import java.util.ArrayList;
import javax.swing.JOptionPane;

public class ControlePonto1 {
    private ArrayList<Funcionario> funcionarios = new ArrayList<>();
    private ArrayList<RegistroPonto> registros = new ArrayList<>();
    private int nextRegistroId = 1;

    public static void main(String[] args) {
        ControlePonto1 sistema = new ControlePonto1();
        sistema.inicializarDados();
        sistema.menuPrincipal();
    }

    private void inicializarDados() {
        // Cadastro de alguns funcionários para teste
        funcionarios.add(new Funcionario(1, "João Silva", "Desenvolvedor", "DEV001"));
        funcionarios.add(new Funcionario(2, "Maria Souza", "Analista", "ANA002"));
        funcionarios.add(new Funcionario(3, "Carlos Oliveira", "Gerente", "GER003"));
    }

    private void menuPrincipal() {
        while (true) {
            String opcao = JOptionPane.showInputDialog(
                "Sistema de Controle de Ponto\n\n" +
                "1. Registrar entrada\n" +
                "2. Registrar saída\n" +
                "3. Listar registros\n" +
                "4. Cadastrar funcionário\n" +
                "5. Sair\n\n" +
                "Escolha uma opção:");

            if (opcao == null || opcao.equals("5")) {
                break;
            }

            switch (opcao) {
                case "1":
                    registrarEntrada();
                    break;
                case "2":
                    registrarSaida();
                    break;
                case "3":
                    listarRegistros();
                    break;
                case "4":
                    cadastrarFuncionario();
                    break;
                default:
                    JOptionPane.showMessageDialog(null, "Opção inválida!");
            }
        }
    }

    private void registrarEntrada() {
        if (funcionarios.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Nenhum funcionário cadastrado!");
            return;
        }

        StringBuilder sb = new StringBuilder("Selecione o funcionário:\n");
        for (int i = 0; i < funcionarios.size(); i++) {
            sb.append(i + 1).append(". ").append(funcionarios.get(i)).append("\n");
        }

        String escolha = JOptionPane.showInputDialog(sb.toString());
        try {
            int index = Integer.parseInt(escolha) - 1;
            if (index >= 0 && index < funcionarios.size()) {
                RegistroPonto registro = new RegistroPonto(
                    nextRegistroId++, 
                    funcionarios.get(index), 
                    LocalDateTime.now()
                );
                registros.add(registro);
                JOptionPane.showMessageDialog(null, 
                    "Entrada registrada para " + funcionarios.get(index).getNome() + 
                    "\nHorário: " + registro.getEntrada());
            } else {
                JOptionPane.showMessageDialog(null, "Índice inválido!");
            }
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(null, "Entrada inválida!");
        }
    }

    private void registrarSaida() {
        if (registros.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Nenhum registro de entrada encontrado!");
            return;
        }

        // Mostrar apenas registros sem saída
        ArrayList<RegistroPonto> registrosAbertos = new ArrayList<>();
        for (RegistroPonto r : registros) {
            if (r.getSaida() == null) {
                registrosAbertos.add(r);
            }
        }

        if (registrosAbertos.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Todos os registros já têm saída!");
            return;
        }

        StringBuilder sb = new StringBuilder("Selecione o registro para registrar saída:\n");
        for (int i = 0; i < registrosAbertos.size(); i++) {
            sb.append(i + 1).append(". ").append(registrosAbertos.get(i).getFuncionario().getNome())
              .append(" - Entrada: ").append(registrosAbertos.get(i).getEntrada()).append("\n");
        }

        String escolha = JOptionPane.showInputDialog(sb.toString());
        try {
            int index = Integer.parseInt(escolha) - 1;
            if (index >= 0 && index < registrosAbertos.size()) {
                RegistroPonto registro = registrosAbertos.get(index);
                registro.registrarSaida(LocalDateTime.now());
                JOptionPane.showMessageDialog(null, 
                    "Saída registrada para " + registro.getFuncionario().getNome() + 
                    "\nHorário: " + registro.getSaida() +
                    "\nHoras trabalhadas: " + registro.calcularHorasTrabalhadas());
            } else {
                JOptionPane.showMessageDialog(null, "Índice inválido!");
            }
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(null, "Entrada inválida!");
        }
    }

    private void listarRegistros() {
        if (registros.isEmpty()) {
            JOptionPane.showMessageDialog(null, "Nenhum registro encontrado!");
            return;
        }

        StringBuilder sb = new StringBuilder("Registros de Ponto:\n\n");
        for (RegistroPonto r : registros) {
            sb.append(r).append("\n\n");
        }

        JOptionPane.showMessageDialog(null, sb.toString());
    }

    private void cadastrarFuncionario() {
        String nome = JOptionPane.showInputDialog("Digite o nome do funcionário:");
        if (nome == null || nome.trim().isEmpty()) return;
        
        String cargo = JOptionPane.showInputDialog("Digite o cargo do funcionário:");
        if (cargo == null || cargo.trim().isEmpty()) return;
        
        String matricula = JOptionPane.showInputDialog("Digite a matrícula do funcionário:");
        if (matricula == null || matricula.trim().isEmpty()) return;
        
        int novoId = funcionarios.isEmpty() ? 1 : funcionarios.get(funcionarios.size() - 1).getId() + 1;
        Funcionario novoFuncionario = new Funcionario(novoId, nome, cargo, matricula);
        funcionarios.add(novoFuncionario);
        
        JOptionPane.showMessageDialog(null, "Funcionário cadastrado com sucesso!\n" + novoFuncionario);
    }
}